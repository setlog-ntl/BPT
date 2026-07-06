"""
실제 남성 성우 톤 5종 — XTTS-v2 내장 화자 + 자연스러운 피치 처리

11. XTTS Damien Black (저음 남성 화자, 한국어로 합성)
12. XTTS Royston Min (성숙한 남성 화자, 한국어)
13. XTTS Viktor Eka (남성 화자, 한국어)
14. Edge InJoon + rubberband -2 semitones + 스튜디오 마스터링 (포먼트 보존, 자연 저음)
15. Edge InJoon + rubberband -1.5 semitones + 워밍 EQ (성우 부스 톤)
"""
import os, sys, subprocess

# Force UTF-8 IO so subprocess captures don't fail on Korean text
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
os.environ["PYTHONIOENCODING"] = "utf-8"

os.environ["COQUI_TOS_AGREED"] = "1"
import torch
_orig_torch_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _orig_torch_load(*args, **kwargs)
torch.load = _patched_load

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "voice_samples")
os.makedirs(OUT, exist_ok=True)

TEXT = "AI는 평균을 주고, 책은 깊이를 줍니다. 이 한 문장이 영상의 핵심입니다."


def xtts_synth(speaker_name, out_wav):
    from TTS.api import TTS
    print(f"  loading XTTS-v2 (speaker={speaker_name})...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    tts.tts_to_file(text=TEXT, speaker=speaker_name, language="ko",
                    file_path=out_wav, split_sentences=True)


def edge_synth_to_mp3(rate, pitch, out_mp3):
    import asyncio, edge_tts
    async def _do():
        comm = edge_tts.Communicate(TEXT, "ko-KR-InJoonNeural", rate=rate, pitch=pitch)
        await comm.save(out_mp3)
    asyncio.run(_do())


def rb_pitch_shift(in_path, out_path, semitones, extra_filters=""):
    """Rubberband: pitch shift while preserving formants (사람 목소리 자연스러움 유지)."""
    chain = f"rubberband=pitch={2**(semitones/12.0):.4f}"
    if extra_filters:
        chain = f"{chain},{extra_filters}"
    cmd = ["ffmpeg", "-y", "-i", in_path, "-af", chain, out_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"    rubberband fail: {(r.stderr or '')[-300:]}")
        # fallback: asetrate (less natural but works)
        ratio = 2**(semitones/12.0)
        chain = f"asetrate=44100*{ratio},aresample=44100"
        if extra_filters:
            chain = f"{chain},{extra_filters}"
        subprocess.run(["ffmpeg", "-y", "-i", in_path, "-af", chain, out_path],
                       check=True, capture_output=True)


def to_mp3(in_wav, out_mp3):
    subprocess.run(["ffmpeg", "-y", "-i", in_wav, "-codec:a", "libmp3lame",
                    "-b:a", "160k", out_mp3],
                   check=True, capture_output=True)


def main():
    print("=== 진짜 성우 톤 5종 ===\n")
    print(f"테스트 문장: \"{TEXT}\"\n")

    # ── 11~13: XTTS-v2 내장 남성 화자
    xtts_speakers = [
        ("Damien Black",  "11_XTTS_Damien_저음남.mp3"),
        ("Royston Min",   "12_XTTS_Royston_성숙남.mp3"),
        ("Viktor Eka",    "13_XTTS_Viktor_중후남.mp3"),
    ]

    # XTTS 1번만 로드해서 3번 합성 (속도)
    from TTS.api import TTS
    tts = None
    for speaker, fname in xtts_speakers:
        out_mp3 = os.path.join(OUT, fname)
        if os.path.exists(out_mp3):
            print(f"  [skip] {fname}")
            continue
        try:
            if tts is None:
                print("  loading XTTS-v2 (one-time)...")
                tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
            tmp_wav = out_mp3.replace(".mp3", ".wav")
            tts.tts_to_file(text=TEXT, speaker=speaker, language="ko",
                            file_path=tmp_wav, split_sentences=True)
            to_mp3(tmp_wav, out_mp3)
            os.remove(tmp_wav)
            print(f"  [ok]  {fname}  (speaker={speaker})")
        except Exception as e:
            print(f"  [fail] {fname}: {e}")

    # ── 14: Edge InJoon + rubberband -2 semitones + 스튜디오 마스터링
    out14 = os.path.join(OUT, "14_InJoon_저음2semi_스튜디오.mp3")
    if not os.path.exists(out14):
        try:
            base = os.path.join(OUT, "_tmp_inj.mp3")
            edge_synth_to_mp3("-2%", "+0Hz", base)
            rb_pitch_shift(base, out14, -2.0,
                # 스튜디오 마스터링: 클린 EQ + 부드러운 컴프
                "highpass=f=70,"
                "equalizer=f=180:width_type=q:width=1.4:g=1.5,"
                "equalizer=f=3000:width_type=q:width=1.5:g=1,"
                "equalizer=f=8000:width_type=q:width=2:g=-2,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=180:makeup=2"
            )
            os.remove(base)
            print(f"  [ok]  14_InJoon_저음2semi_스튜디오.mp3  (rubberband -2 semi + 스튜디오 마스터링)")
        except Exception as e:
            print(f"  [fail] 14: {e}")

    # ── 15: Edge InJoon + rubberband -1.5 semitones + 부스 워밍
    out15 = os.path.join(OUT, "15_InJoon_저음1_5semi_부스.mp3")
    if not os.path.exists(out15):
        try:
            base = os.path.join(OUT, "_tmp_inj2.mp3")
            edge_synth_to_mp3("-3%", "+0Hz", base)
            rb_pitch_shift(base, out15, -1.5,
                # 성우 부스 톤: 워밍 + 명료함
                "highpass=f=80,"
                "equalizer=f=220:width_type=q:width=1.3:g=2,"
                "equalizer=f=2500:width_type=q:width=1.5:g=1.2,"
                "acompressor=threshold=-18dB:ratio=2.8:attack=12:release=160:makeup=2"
            )
            os.remove(base)
            print(f"  [ok]  15_InJoon_저음1_5semi_부스.mp3  (rubberband -1.5 semi + 부스 워밍)")
        except Exception as e:
            print(f"  [fail] 15: {e}")

    print(f"\n샘플 폴더: {OUT}")
    new = ["11_XTTS_Damien_저음남.mp3", "12_XTTS_Royston_성숙남.mp3",
           "13_XTTS_Viktor_중후남.mp3", "14_InJoon_저음2semi_스튜디오.mp3",
           "15_InJoon_저음1_5semi_부스.mp3"]
    for f in new:
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            print(f"  {f}  ({os.path.getsize(p)//1024}KB)")


if __name__ == "__main__":
    main()
