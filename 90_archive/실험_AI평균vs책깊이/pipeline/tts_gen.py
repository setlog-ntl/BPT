"""
Edge TTS 한국어 내레이션 합성기 v4.1 — 보이스+속도+마스터링 조합

전략 (Edge TTS는 SSML 지원이 제한적이라 평문+rate/pitch로 자연스러움 추구):
- VOICE: ko-KR-SeoHyeonNeural (차분 신뢰감 여성)
- RATE: -3% (약간 느리게 = 인사이트 톤)
- 핵심 자연스러움 부여는 compose_ffmpeg.py의 마스터링 체인이 담당
  · HPF + 컴프 + de-ess + LUFS 노멀라이즈
  · BGM 사이드체인 더킹 (음성 시 BGM 자동 -8dB)
"""
import asyncio
import os
import edge_tts
from scenes import SCENES

VOICE = "ko-KR-InJoonNeural"  # 옵션: ko-KR-InJoonNeural(남), ko-KR-SunHiNeural, ko-KR-HyunsuMultilingualNeural
RATE  = "-3%"
PITCH = "+0Hz"

OUT_DIR = os.path.join(os.path.dirname(__file__), "audio")


async def synth_one(scene, force=False):
    out = os.path.join(OUT_DIR, f"scene_{scene['id']:02d}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1024 and not force:
        print(f"  [skip] scene_{scene['id']:02d}.mp3")
        return out
    text = scene["narration"]
    comm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await comm.save(out)
    size = os.path.getsize(out)
    print(f"  [ok]   scene_{scene['id']:02d}.mp3  ({size//1024}KB)  {text[:30]}...")
    return out


async def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"  Voice: {VOICE}")
    print(f"  Rate: {RATE}, Pitch: {PITCH}")
    print()
    for sc in SCENES:
        try:
            await synth_one(sc)
        except Exception as e:
            print(f"  [FAIL] scene_{sc['id']:02d}: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
