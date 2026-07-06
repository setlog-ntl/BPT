"""V10 TTS — 별도 스크립트로 안전하게"""
import asyncio, os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except: pass
import edge_tts
from scenes_shorts_v10 import SCENES

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_v10")
os.makedirs(OUT_DIR, exist_ok=True)

VOICE = "ko-KR-InJoonNeural"
RATE = "-3%"
PITCH = "+0Hz"


async def main():
    print(f"Voice: {VOICE} {RATE}")
    for sc in SCENES:
        out = os.path.join(OUT_DIR, f"scene_{sc['id']:02d}.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 1024:
            print(f"  [skip] scene_{sc['id']:02d}")
            continue
        comm = edge_tts.Communicate(sc["narration"], VOICE, rate=RATE, pitch=PITCH)
        await comm.save(out)
        sz = os.path.getsize(out)
        print(f"  [ok]   scene_{sc['id']:02d}.mp3 ({sz//1024}KB) {sc['narration'][:30]}")


if __name__ == "__main__":
    asyncio.run(main())
