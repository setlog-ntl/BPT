"""
MeloTTS 한국어 합성 — KSS 데이터셋 학습 monolingual 모델

- 한국어 전용으로 학습되어 발음 정확도가 XTTS 다국어보다 훨씬 좋음
- VITS 아키텍처 → CPU에서 빠름
- 단일 화자 (KSS 여성 표준 발음)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "audio")
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    print("[melo] Loading MeloTTS library...")
    try:
        from melo.api import TTS
    except ImportError as e:
        print(f"  [ERROR] MeloTTS not installed: {e}")
        print("  Install: pip install git+https://github.com/myshell-ai/MeloTTS.git")
        print("  Then:   python -m unidic download")
        sys.exit(1)

    print("[melo] Loading Korean model (first time = downloads ~300MB)...")
    model = TTS(language='KR', device='cpu')
    speaker_ids = model.hps.data.spk2id
    print(f"  Speakers: {speaker_ids}")
    speaker_id = list(speaker_ids.values())[0]

    from scenes import SCENES
    for sc in SCENES:
        out = os.path.join(OUT_DIR, f"scene_{sc['id']:02d}.wav")
        if os.path.exists(out) and os.path.getsize(out) > 1024:
            print(f"  [skip] {out}")
            continue
        text = sc["narration"]
        try:
            # speed=1.0 default. We use 0.92 (slower) for thoughtful tone
            model.tts_to_file(text, speaker_id, out, speed=0.92)
            size = os.path.getsize(out)
            print(f"  [ok]   scene_{sc['id']:02d}.wav ({size//1024}KB) {text[:30]}...")
        except Exception as e:
            print(f"  [FAIL] scene_{sc['id']:02d}: {e}")
            raise


if __name__ == "__main__":
    main()
