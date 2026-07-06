"""
원클릭 오케스트레이터 v2 — 사진 배경 + 자연스러운 TTS

흐름:
  1) loremflickr.com 에서 씬별 사진 38장 다운로드 (image_fetch.py)
  2) slides_v2 로 사진 배경 + 키네틱 타이포 슬라이드 38장
  3) 절차 BGM 10분 wav
  4) Edge TTS 한국어 (ko-KR-HyunsuMultilingualNeural — 자연스러운 신규 보이스)
  5) ffmpeg 합성 + 자막 burn-in
"""
import argparse, os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def step(name):
    print("\n" + "=" * 60); print(name); print("=" * 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-tts", action="store_true")
    ap.add_argument("--no-burn", action="store_true")
    ap.add_argument("--no-images", action="store_true",
                    help="이미지 다운로드 스킵 (그라데이션 배경)")
    ap.add_argument("--clean", action="store_true",
                    help="기존 슬라이드/오디오 캐시 삭제하고 재생성")
    args = ap.parse_args()

    if args.clean:
        import shutil
        for d in ["slides", "audio", "tmp_render"]:
            full = os.path.join(HERE, d)
            if os.path.exists(full):
                shutil.rmtree(full, ignore_errors=True)
                print(f"  [clean] removed {d}/")

    # 1) IMAGES
    if not args.no_images:
        step("[1/5] 씬별 이미지 다운로드 (loremflickr.com)")
        from image_fetch import main as img_main
        img_main()
    else:
        print("\n[1/5] 이미지 스킵")

    # 2) SLIDES (v2)
    step("[2/5] 슬라이드 렌더링 v2 — 사진 배경 + 키네틱 타이포")
    from slides_v2 import render_all
    from scenes import SCENES
    render_all(SCENES, os.path.join(HERE, "slides"))
    print(f"  ok. ({len(SCENES)} slides)")

    # 3) BGM
    step("[3/5] 절차 BGM 10분 생성")
    from bgm_gen import make_track
    bgm_path = os.path.join(HERE, "audio", "bgm.wav")
    os.makedirs(os.path.dirname(bgm_path), exist_ok=True)
    if not os.path.exists(bgm_path):
        make_track(620, bgm_path)
    print(f"  ok: {bgm_path}")

    # 4) TTS
    silent = args.no_tts
    if args.no_tts:
        print("\n[4/5] TTS 스킵 (--no-tts)")
    else:
        step("[4/5] Edge TTS 한국어 — Hyunsu Multilingual (자연스러운 보이스)")
        try:
            import asyncio
            from tts_gen import main as tts_main
            asyncio.run(tts_main())
            print("  ok.")
        except Exception as e:
            print(f"  WARN: TTS 실패 → {e}")
            silent = True

    # 5) Compose
    step("[5/5] ffmpeg 영상 합성 + 자막 burn-in")
    cmd = [sys.executable, os.path.join(HERE, "compose_ffmpeg.py")]
    if silent:
        cmd.append("--silent")
    if args.no_burn:
        cmd.append("--no-burn")
    subprocess.run(cmd, check=True)
    print("\n[DONE] pipeline\\output\\ 폴더 확인")


if __name__ == "__main__":
    main()

