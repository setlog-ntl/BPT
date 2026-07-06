"""
남성 보이스 5종 샘플 — 5가지 다른 캐릭터

6. 묵직한 라디오 DJ — 깊은 피치 + 따뜻한 EQ + 적당한 리버브
7. 활기찬 젊은 남성 — 빠른 속도 + 높은 피치 + 밝은 톤
8. 다큐멘터리 내레이터 — 매우 느린 속도 + 낮은 피치 + 정교한 발음
9. 친근한 친구 톤 — Hyunsu 정상 + 살짝 높은 피치 + 작은 룸 리버브
10. 저음 뉴스 앵커 — 매우 낮은 피치 + 강한 컴프레서 + 명료함 부스트
"""
import asyncio, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "voice_samples")
os.makedirs(OUT, exist_ok=True)

TEXT = "AI는 평균을 주고, 책은 깊이를 줍니다. 이 한 문장이 영상의 핵심입니다."


async def edge_synth(voice, rate, pitch, out_path):
    import edge_tts
    comm = edge_tts.Communicate(TEXT, voice, rate=rate, pitch=pitch)
    await comm.save(out_path)


def post_process(in_path, out_path, filters):
    cmd = ["ffmpeg", "-y", "-i", in_path, "-af", filters, out_path]
    subprocess.run(cmd, check=True, capture_output=True)


async def main():
    print("=== 남성 5종 추가 샘플 ===\n")
    print(f"테스트 문장: \"{TEXT}\"\n")

    # Generate base voices first
    base_inj = os.path.join(OUT, "_tmp_inj_base.mp3")
    base_hyu = os.path.join(OUT, "_tmp_hyu_base.mp3")

    if not os.path.exists(base_inj):
        await edge_synth("ko-KR-InJoonNeural", "+0%", "+0Hz", base_inj)
    if not os.path.exists(base_hyu):
        await edge_synth("ko-KR-HyunsuMultilingualNeural", "+0%", "+0Hz", base_hyu)

    # ── Sample 6: 묵직한 라디오 DJ
    out = os.path.join(OUT, "06_라디오DJ_묵직.mp3")
    await edge_synth("ko-KR-InJoonNeural", "-8%", "-3Hz", base_inj.replace("base", "s6"))
    post_process(
        base_inj.replace("base", "s6"), out,
        # 피치 다운 더 + 풍성한 리버브 + 워밍 EQ
        "asetrate=44100*0.95,aresample=44100,"
        "equalizer=f=150:width_type=q:width=1.4:g=3,"
        "equalizer=f=400:width_type=q:width=1.8:g=1,"
        "equalizer=f=8000:width_type=q:width=2:g=-3,"
        "aecho=0.7:0.5:80:0.35"
    )
    print(f"  [ok]  06_라디오DJ_묵직.mp3")

    # ── Sample 7: 활기찬 젊은 남성
    out = os.path.join(OUT, "07_젊은남성_활기.mp3")
    await edge_synth("ko-KR-InJoonNeural", "+8%", "+5Hz", base_inj.replace("base", "s7"))
    post_process(
        base_inj.replace("base", "s7"), out,
        # 피치 더 위로 + 밝은 EQ
        "asetrate=44100*1.05,aresample=44100,"
        "equalizer=f=2500:width_type=q:width=1.5:g=2,"
        "equalizer=f=5000:width_type=q:width=2:g=1.5"
    )
    print(f"  [ok]  07_젊은남성_활기.mp3")

    # ── Sample 8: 다큐멘터리 내레이터
    out = os.path.join(OUT, "08_다큐_정교.mp3")
    await edge_synth("ko-KR-InJoonNeural", "-15%", "-2Hz", base_inj.replace("base", "s8"))
    post_process(
        base_inj.replace("base", "s8"), out,
        # 약간의 피치 다운 + 명료함 (리버브 없음)
        "asetrate=44100*0.97,aresample=44100,"
        "equalizer=f=200:width_type=q:width=1.4:g=1,"
        "equalizer=f=3500:width_type=q:width=1.5:g=2,"
        "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=180:makeup=2"
    )
    print(f"  [ok]  08_다큐_정교.mp3")

    # ── Sample 9: 친근한 친구 톤
    out = os.path.join(OUT, "09_친근한_친구톤.mp3")
    await edge_synth("ko-KR-HyunsuMultilingualNeural", "+3%", "+2Hz", base_hyu.replace("base", "s9"))
    post_process(
        base_hyu.replace("base", "s9"), out,
        # 작은 룸 리버브 + 살짝 따뜻
        "equalizer=f=300:width_type=q:width=1.2:g=1,"
        "aecho=0.5:0.4:35:0.18"
    )
    print(f"  [ok]  09_친근한_친구톤.mp3")

    # ── Sample 10: 저음 뉴스 앵커
    out = os.path.join(OUT, "10_뉴스앵커_저음.mp3")
    await edge_synth("ko-KR-InJoonNeural", "-3%", "-5Hz", base_inj.replace("base", "s10"))
    post_process(
        base_inj.replace("base", "s10"), out,
        # 매우 낮은 피치 + 강 컴프 + 프레전스
        "asetrate=44100*0.92,aresample=44100,"
        "equalizer=f=180:width_type=q:width=1.3:g=2.5,"
        "equalizer=f=4000:width_type=q:width=1.5:g=2,"
        "acompressor=threshold=-16dB:ratio=4:attack=10:release=140:makeup=3"
    )
    print(f"  [ok]  10_뉴스앵커_저음.mp3")

    # cleanup tmp
    for f in os.listdir(OUT):
        if f.startswith("_tmp_") or "_s6.mp3" in f or "_s7.mp3" in f or "_s8.mp3" in f or "_s9.mp3" in f or "_s10.mp3" in f:
            try: os.remove(os.path.join(OUT, f))
            except: pass

    print(f"\n샘플 폴더: {OUT}")
    for f in sorted(os.listdir(OUT)):
        if not f.startswith("_") and f.endswith(".mp3"):
            size = os.path.getsize(os.path.join(OUT, f))
            print(f"  {f}  ({size//1024}KB)")


if __name__ == "__main__":
    asyncio.run(main())
