"""
진짜 성우 톤 5종 — v2 (XTTS speaker auto-discover)

XTTS-v2의 실제 사용 가능한 male speakers를 자동으로 찾아서 처음 3명 사용.
14, 15는 이미 생성됨 — 11~13만 새로 생성.
"""
import os, sys, subprocess

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except: pass
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["COQUI_TOS_AGREED"] = "1"
import torch
_orig = torch.load
torch.load = lambda *a, **k: _orig(*a, **{**k, "weights_only": False})

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "voice_samples")
os.makedirs(OUT, exist_ok=True)

TEXT = "AI는 평균을 주고, 책은 깊이를 줍니다. 이 한 문장이 영상의 핵심입니다."

# Curated XTTS-v2 male speakers known to produce deep/mature voiceover quality
MALE_SPEAKERS = [
    ("Damien Black",       "11_XTTS_Damien_저음남"),
    ("Royston Min",        "12_XTTS_Royston_성숙남"),
    ("Viktor Eka",         "13_XTTS_Viktor_중후남"),
    # backups in case any of above fails
    ("Andrew Chipper",     "11b_XTTS_Andrew"),
    ("Badr Odhiambo",      "12b_XTTS_Badr"),
    ("Craig Gutsy",        "13b_XTTS_Craig"),
    ("Dionisio Schuyler",  "_alt"),
    ("Wulf Carlevaro",     "_alt"),
    ("Ludvig Milivoj",     "_alt"),
]

def to_mp3(in_wav, out_mp3):
    subprocess.run(["ffmpeg", "-y", "-i", in_wav, "-codec:a", "libmp3lame",
                    "-b:a", "160k", out_mp3], check=True, capture_output=True)


def main():
    print("=== XTTS 남성 화자 11~13 합성 ===")
    print(f"텍스트: \"{TEXT}\"\n")

    print("loading XTTS-v2 model...")
    from TTS.api import TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

    # Try to inspect available speakers
    try:
        # Coqui TTS API: tts.synthesizer.tts_model.speaker_manager.speakers
        speakers = list(tts.synthesizer.tts_model.speaker_manager.name_to_id.keys())
        print(f"  사용 가능한 speakers: {len(speakers)}명")
        male_keywords = ["Damien", "Royston", "Viktor", "Andrew", "Badr", "Craig",
                          "Dionisio", "Wulf", "Ludvig", "Adde", "Filip", "Damjan",
                          "Kazuhiko", "Suad", "Torcull", "Zacharie", "Ilkin",
                          "Baldur", "Abrahan", "Gilberto"]
        male_avail = [s for s in speakers if any(k in s for k in male_keywords)]
        print(f"  남성으로 추정: {male_avail[:8]}...")
    except Exception as e:
        print(f"  speaker enumerate fail: {e}")
        male_avail = ["Damien Black", "Royston Min", "Viktor Eka"]

    targets = []
    needed = 3
    for spk, label in MALE_SPEAKERS:
        if len(targets) >= needed: break
        if spk in male_avail or spk in [m for m in MALE_SPEAKERS]:
            targets.append((spk, label))
    if not targets:
        targets = [(s, f"1{i+1}_XTTS_{s.split()[0]}") for i, s in enumerate(male_avail[:3])]

    print(f"\n  최종 합성 대상: {[(s, l) for s, l in targets[:3]]}\n")

    for spk, label in targets[:3]:
        out_mp3 = os.path.join(OUT, f"{label}.mp3")
        if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1024:
            print(f"  [skip] {label}.mp3")
            continue
        try:
            tmp_wav = out_mp3.replace(".mp3", ".wav")
            tts.tts_to_file(text=TEXT, speaker=spk, language="ko",
                            file_path=tmp_wav, split_sentences=True)
            to_mp3(tmp_wav, out_mp3)
            try: os.remove(tmp_wav)
            except: pass
            print(f"  [ok]  {label}.mp3  (speaker={spk})")
        except Exception as e:
            print(f"  [fail] {label} ({spk}): {str(e)[:200]}")

    print(f"\n완료. 폴더: {OUT}")
    for f in sorted(os.listdir(OUT)):
        if f.startswith(("11", "12", "13")) and f.endswith(".mp3"):
            print(f"  {f}  ({os.path.getsize(os.path.join(OUT, f))//1024}KB)")


if __name__ == "__main__":
    main()
