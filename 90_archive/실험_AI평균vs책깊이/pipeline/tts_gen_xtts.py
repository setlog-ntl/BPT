"""
Coqui XTTS-v2 한국어 합성 — 보이스 클로닝 기반

· XTTS-v2: Coqui AI 2024 SOTA 오픈소스 보이스 클로닝 모델 (다국어, 한국어 포함)
· 6초 reference 오디오로 그 목소리로 합성
· CPU에서 동작 (느리지만 무료)

reference voice 우선순위:
  1. ./reference_voice.wav   (사용자가 직접 둔 음성, 6~10초)
  2. ./reference_voice.mp3
  3. 모델 기본 한국어 화자 fallback (XTTS의 default speakers 중)
"""
import os, sys, glob
os.environ["COQUI_TOS_AGREED"] = "1"

# PyTorch 2.6+ weights_only=True default → XTTS checkpoint load 실패 우회
import torch
_orig_torch_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _orig_torch_load(*args, **kwargs)
torch.load = _patched_load

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "audio")
os.makedirs(OUT_DIR, exist_ok=True)


def find_reference_voice():
    """reference_voice.wav 또는 reference_voice.mp3 검색"""
    for ext in ("wav", "mp3", "m4a", "ogg"):
        p = os.path.join(HERE, f"reference_voice.{ext}")
        if os.path.exists(p):
            return p
    return None


def main():
    print("[xtts] Loading TTS library (first time = slow)...")
    try:
        from TTS.api import TTS
    except ImportError:
        print("  [ERROR] TTS not installed. Run: pip install TTS==0.22.0")
        sys.exit(1)

    print("[xtts] Loading XTTS-v2 model (first time = downloads ~2GB)...")
    # use the public XTTS-v2 model
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

    ref = find_reference_voice()
    if ref:
        print(f"[xtts] Using reference voice: {ref}")
    else:
        print("[xtts] No reference voice found. Using model default.")
        # XTTS-v2 has built-in speaker embeddings; we'll use a Korean-suitable one
        ref = None  # will use speaker_wav=None which requires speaker name

    from scenes import SCENES
    for sc in SCENES:
        out = os.path.join(OUT_DIR, f"scene_{sc['id']:02d}.wav")
        if os.path.exists(out) and os.path.getsize(out) > 1024:
            print(f"  [skip] {out}")
            continue
        text = sc["narration"]
        try:
            if ref:
                tts.tts_to_file(text=text, speaker_wav=ref, language="ko",
                                file_path=out, split_sentences=True)
            else:
                # use a built-in speaker (XTTS supports speakers like "Damien Black")
                tts.tts_to_file(text=text, speaker="Damien Black", language="ko",
                                file_path=out, split_sentences=True)
            size = os.path.getsize(out)
            print(f"  [ok]   scene_{sc['id']:02d}.wav ({size//1024}KB) {text[:30]}...")
        except Exception as e:
            print(f"  [FAIL] scene_{sc['id']:02d}: {e}")
            raise


if __name__ == "__main__":
    main()
