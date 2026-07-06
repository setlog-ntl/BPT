"""
11~13: Edge TTS rubberband 변형으로 3가지 자연스러운 깊은 남성 톤
(XTTS가 환경 문제로 실패해서 대체)

11. 클린 저음 — InJoon, rubberband -2.5 semi, 미니멀 처리 (자연스러운 깊이)
12. 성숙한 톤 — Hyunsu, rubberband -1.5 semi, 워밍 체스트 EQ
13. 방송 보이스 — InJoon, rubberband -1 semi + 강 컴프 + 명료함 부스트
"""
import os, sys, subprocess, asyncio
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except: pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "voice_samples")
os.makedirs(OUT, exist_ok=True)

TEXT = "AI는 평균을 주고, 책은 깊이를 줍니다. 이 한 문장이 영상의 핵심입니다."


async def edge_synth(voice, rate, pitch, out_mp3):
    import edge_tts
    comm = edge_tts.Communicate(TEXT, voice, rate=rate, pitch=pitch)
    await comm.save(out_mp3)


def rb_shift(in_path, out_path, semitones, extra_filters=""):
    pitch_ratio = 2 ** (semitones / 12.0)
    chain = f"rubberband=pitch={pitch_ratio:.4f}"
    if extra_filters:
        chain = chain + "," + extra_filters
    cmd = ["ffmpeg", "-y", "-i", in_path, "-af", chain, out_path]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        # fallback to atempo+asetrate
        ratio = 2 ** (semitones / 12.0)
        chain2 = f"asetrate=44100*{ratio},aresample=44100,atempo={1/ratio:.4f}"
        if extra_filters:
            chain2 = chain2 + "," + extra_filters
        subprocess.run(["ffmpeg", "-y", "-i", in_path, "-af", chain2, out_path],
                       check=True, capture_output=True)


async def main():
    print("=== 11~13: Edge TTS rubberband 변형 ===\n")

    # 11
    out11 = os.path.join(OUT, "11_클린_자연저음.mp3")
    if not os.path.exists(out11):
        tmp = os.path.join(OUT, "_t11.mp3")
        await edge_synth("ko-KR-InJoonNeural", "-2%", "+0Hz", tmp)
        # minimal processing
        rb_shift(tmp, out11, -2.5,
                 "highpass=f=70,equalizer=f=200:width_type=q:width=1.4:g=1")
        os.remove(tmp)
        print("  [ok]  11_클린_자연저음.mp3  (rubberband -2.5 semi, 미니멀 EQ)")

    # 12
    out12 = os.path.join(OUT, "12_성숙한_체스트톤.mp3")
    if not os.path.exists(out12):
        tmp = os.path.join(OUT, "_t12.mp3")
        await edge_synth("ko-KR-HyunsuMultilingualNeural", "-3%", "+0Hz", tmp)
        rb_shift(tmp, out12, -1.5,
                 "highpass=f=70,"
                 "equalizer=f=180:width_type=q:width=1.3:g=2.5,"
                 "equalizer=f=400:width_type=q:width=1.5:g=1.2,"
                 "equalizer=f=8000:width_type=q:width=2:g=-2")
        os.remove(tmp)
        print("  [ok]  12_성숙한_체스트톤.mp3  (rubberband -1.5 semi, 워밍 EQ)")

    # 13
    out13 = os.path.join(OUT, "13_방송보이스.mp3")
    if not os.path.exists(out13):
        tmp = os.path.join(OUT, "_t13.mp3")
        await edge_synth("ko-KR-InJoonNeural", "-3%", "+0Hz", tmp)
        rb_shift(tmp, out13, -1.0,
                 "highpass=f=80,"
                 "equalizer=f=200:width_type=q:width=1.4:g=1.5,"
                 "equalizer=f=3500:width_type=q:width=1.5:g=2,"
                 "acompressor=threshold=-16dB:ratio=4:attack=10:release=130:makeup=3")
        os.remove(tmp)
        print("  [ok]  13_방송보이스.mp3  (rubberband -1 semi + 강 컴프)")

    print("\n완료. voice_samples 폴더 11~15 모두 준비됨")


if __name__ == "__main__":
    asyncio.run(main())
