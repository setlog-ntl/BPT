"""
5가지 보이스 샘플 생성 — 같은 문장, 다른 음색

Sample 1: 차분한 여성 (Edge TTS SunHi) — 기본
Sample 2: 차분한 남성 (Edge TTS InJoon) — 신뢰감
Sample 3: 다국어 남성 (Edge TTS Hyunsu) — 깔끔
Sample 4: 한국어 전용 여성 (MeloTTS KSS) — 정확한 발음
Sample 5: 깊고 묵직한 내레이터 (Edge TTS InJoon + 피치 -3Hz, 속도 -10%, 약한 리버브)
"""
import asyncio, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "voice_samples")
os.makedirs(OUT, exist_ok=True)

TEXT = "AI는 평균을 주고, 책은 깊이를 줍니다. 이 한 문장이 영상의 핵심입니다."


async def edge_synth(voice, rate, pitch, out_path):
    import edge_tts
    comm = edge_tts.Communicate(TEXT, voice, rate=rate, pitch=pitch)
    await comm.save(out_path)


def melo_synth(out_path):
    """MeloTTS Korean."""
    from melo.api import TTS
    model = TTS(language='KR', device='cpu')
    speaker_id = list(model.hps.data.spk2id.values())[0]
    model.tts_to_file(TEXT, speaker_id, out_path, speed=0.95)


def post_process_deep(in_path, out_path):
    """깊고 묵직한 내레이터 효과: 피치 -3Hz 톤 다운, 약한 리버브"""
    cmd = [
        "ffmpeg", "-y", "-i", in_path,
        "-af",
        # 피치 down + 약한 리버브 + 워밍 EQ
        "asetrate=44100*0.94,aresample=44100,"
        "equalizer=f=200:width_type=q:width=1.4:g=2,"
        "equalizer=f=8000:width_type=q:width=2:g=-2,"
        "aecho=0.6:0.5:60:0.25",
        out_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)


async def main():
    print("=== 5가지 음성 샘플 생성 ===\n")
    print(f"테스트 문장: \"{TEXT}\"\n")

    samples = [
        ("01_차분한여성_SunHi.mp3",      "ko-KR-SunHiNeural",      "+0%",  "+0Hz"),
        ("02_차분한남성_InJoon.mp3",     "ko-KR-InJoonNeural",     "-3%",  "+0Hz"),
        ("03_다국어남성_Hyunsu.mp3",     "ko-KR-HyunsuMultilingualNeural", "+0%", "+0Hz"),
    ]

    for fname, voice, rate, pitch in samples:
        out = os.path.join(OUT, fname)
        if os.path.exists(out): 
            print(f"  [skip] {fname}")
            continue
        try:
            await edge_synth(voice, rate, pitch, out)
            print(f"  [ok]  {fname}  ({voice}, rate={rate}, pitch={pitch})")
        except Exception as e:
            print(f"  [fail] {fname}: {e}")

    # Sample 4: MeloTTS Korean
    out4 = os.path.join(OUT, "04_한국어전용_MeloTTS.mp3")
    if not os.path.exists(out4):
        try:
            wav4 = out4.replace(".mp3", ".wav")
            melo_synth(wav4)
            subprocess.run(["ffmpeg", "-y", "-i", wav4, "-codec:a", "libmp3lame", "-b:a", "128k", out4],
                           check=True, capture_output=True)
            os.remove(wav4)
            print(f"  [ok]  04_한국어전용_MeloTTS.mp3  (KSS Korean monolingual)")
        except Exception as e:
            print(f"  [fail] MeloTTS sample: {e}")

    # Sample 5: deep narrator (post-process Sample 2)
    out5 = os.path.join(OUT, "05_묵직한내레이터_InJoon변형.mp3")
    if not os.path.exists(out5):
        try:
            base = os.path.join(OUT, "02_차분한남성_InJoon.mp3")
            post_process_deep(base, out5)
            print(f"  [ok]  05_묵직한내레이터_InJoon변형.mp3  (InJoon + 피치 down + 리버브)")
        except Exception as e:
            print(f"  [fail] sample 5: {e}")

    print(f"\n샘플 폴더: {OUT}")
    for f in sorted(os.listdir(OUT)):
        size = os.path.getsize(os.path.join(OUT, f))
        print(f"  {f}  ({size//1024}KB)")


if __name__ == "__main__":
    asyncio.run(main())
