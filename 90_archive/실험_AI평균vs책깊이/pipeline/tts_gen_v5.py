"""
Edge TTS v5 — 문장 단위 분리 합성 + 룰 기반 prosody

씬 단위 단조로운 합성에서 벗어나, 한 씬을 N개 문장으로 분해해서
각 문장에 다른 rate/pitch를 적용한 후 자연스러운 호흡으로 이어붙임.

분류 규칙 (자동):
  의문문(?끝): rate=-8%, gap=600ms
  짧은 임팩트(<20자): rate=-10%, gap=500ms
  핵심문구 포함: rate=-12%, gap=500ms (앞 200ms 추가 pause)
  새 챕터 첫 문장: rate=-5%, pitch=+3Hz
  정리·결론 시작어: rate=-8%, pitch=-2Hz, gap=700ms
  긴 설명(>40자): rate=+0%, gap=400ms
  일반: rate=-3%, gap=350ms
"""
import asyncio, os, re, subprocess
import edge_tts
from scenes import SCENES

VOICE = "ko-KR-InJoonNeural"
PITCH = "+0Hz"

OUT_DIR = os.path.join(os.path.dirname(__file__), "audio")
TMP_DIR = os.path.join(os.path.dirname(__file__), "audio_sentences")

# 정리·결론 신호어
CLOSURE_STARTERS = ["정리하면", "결국", "다시 말해", "즉,", "한마디로",
                     "다시 한 번", "그래서", "오늘"]
# 새 챕터 첫 문장 키워드 (대본 패턴 기반)
CHAPTER_OPENERS = ["첫 번째", "두 번째", "세 번째", "네 번째", "다섯 번째",
                    "이유 1", "이유 2", "이유 3", "이유 4", "이유 5",
                    "첫째", "둘째", "셋째"]


def split_sentences(text):
    """한국어 문장 분리. 종결어미 + 구두점 기준."""
    # 끝 토큰 + .?! 다음에 공백
    parts = re.split(r'(?<=[다요까네라죠고됨음])\.\s+|(?<=\?)\s+|(?<=!)\s+', text)
    parts = [p.strip() for p in parts if p.strip()]
    # 끝에 구두점 없으면 . 추가
    out = []
    for p in parts:
        if not p.endswith(('.', '?', '!')):
            p += '.'
        out.append(p)
    return out


def classify(sentence, scene, idx, total):
    """문장 → (rate, pitch, post_gap_ms, pre_gap_ms)"""
    s = sentence.strip()
    big_phrases = [scene.get("big1", ""), scene.get("big2", "")]
    big_phrases = [b.strip() for b in big_phrases if b and len(b) > 1]

    rate = "-3%"; pitch = PITCH; gap = 350; pre = 0

    if s.endswith("?"):
        rate, pitch, gap = "-8%", "+0Hz", 600
    elif any(s.startswith(c) for c in CLOSURE_STARTERS):
        rate, pitch, gap = "-8%", "-2Hz", 700
    elif any(s.startswith(c) for c in CHAPTER_OPENERS):
        rate, pitch, gap = "-5%", "+3Hz", 400
    elif any(bp in s for bp in big_phrases):
        rate, pitch, gap = "-10%", "+0Hz", 500
        pre = 200  # 핵심 문구 앞에 살짝 멈춤
    elif len(s) < 20:
        rate, gap = "-10%", 500
    elif len(s) > 40:
        rate, gap = "+0%", 400
    # else default

    # 첫 문장이면 pitch 살짝 위 (주의 환기)
    if idx == 0 and pitch == PITCH:
        pitch = "+2Hz"

    # 마지막 문장이면 gap 좀 더 길게 (씬 마무리)
    if idx == total - 1:
        gap = max(gap, 500)

    return rate, pitch, gap, pre


async def synth_sentence(text, rate, pitch, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
        return out_path
    comm = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
    await comm.save(out_path)
    return out_path


def concat_with_gaps(sentence_files, gaps_ms, out_path):
    """sentence files + per-sentence post-gap → single mp3 via ffmpeg.
    sentence_files: [path1, path2, ...]
    gaps_ms: [post_gap_after_path1, post_gap_after_path2, ...]
    """
    # Build concat with silence between using ffmpeg filter_complex
    # Approach: decode each, append silence after, concatenate
    inputs = []
    filter_parts = []
    for i, p in enumerate(sentence_files):
        inputs += ["-i", p]

    # Each input goes through afade (natural edges), then we append silence
    n = len(sentence_files)
    parts = []
    for i in range(n):
        gap_s = gaps_ms[i] / 1000.0
        # adelay/apad approach: we use [Xa] to mark and concat
        parts.append(
            f"[{i}:a]afade=t=in:st=0:d=0.04,"
            f"afade=t=out:st=$end_{i}$:d=0.12,"
            f"apad=pad_dur={gap_s:.3f}[s{i}]"
        )
    # Replace $end_N$ placeholders by computing each clip duration via ffprobe (faster: just use atrim with stream end)
    # Simpler: use atrim by setting end as the actual mp3 length; but here we just rely on apad
    # For fade-out timing, use the duration from ffprobe
    durs = []
    for p in sentence_files:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=nw=1:nk=1", p],
                           capture_output=True, text=True)
        durs.append(float(r.stdout.strip()))

    # Rebuild filter with real durations
    filter_str = ""
    for i in range(n):
        gap_s = gaps_ms[i] / 1000.0
        end_t = max(0.0, durs[i] - 0.12)
        filter_str += (
            f"[{i}:a]afade=t=in:st=0:d=0.04,"
            f"afade=t=out:st={end_t:.3f}:d=0.12,"
            f"apad=pad_dur={gap_s:.3f}[s{i}];"
        )
    concat_inputs = "".join(f"[s{i}]" for i in range(n))
    filter_str += f"{concat_inputs}concat=n={n}:v=0:a=1[aout]"

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[aout]", "-ar", "44100", "-ac", "2",
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("concat fail:", (r.stderr or "")[-400:])
        raise RuntimeError("concat failed")
    return out_path


async def synth_scene(scene, force=False):
    out = os.path.join(OUT_DIR, f"scene_{scene['id']:02d}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1024 and not force:
        print(f"  [skip] scene_{scene['id']:02d}.mp3")
        return out
    sentences = split_sentences(scene["narration"])
    if not sentences:
        return None

    sent_paths = []
    gaps = []
    os.makedirs(TMP_DIR, exist_ok=True)
    for i, sent in enumerate(sentences):
        rate, pitch, post_gap, pre_gap = classify(sent, scene, i, len(sentences))
        sent_path = os.path.join(TMP_DIR, f"s_{scene['id']:02d}_{i:02d}.mp3")
        await synth_sentence(sent, rate, pitch, sent_path)
        # If pre_gap, we add it to the *previous* sentence's post_gap
        if pre_gap > 0 and gaps:
            gaps[-1] += pre_gap
        sent_paths.append(sent_path)
        gaps.append(post_gap)

    concat_with_gaps(sent_paths, gaps, out)
    print(f"  [ok]   scene_{scene['id']:02d}.mp3 ({len(sentences)} sents, {sum(gaps)}ms breaths)")
    return out


async def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"  Voice: {VOICE} · sentence-level prosody")
    for sc in SCENES:
        try:
            await synth_scene(sc)
        except Exception as e:
            print(f"  [FAIL] scene_{sc['id']:02d}: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
