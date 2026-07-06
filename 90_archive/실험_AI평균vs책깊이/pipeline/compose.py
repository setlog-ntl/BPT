"""
moviepy 영상 합성기

흐름:
  1) 씬별 TTS mp3 길이를 측정 (없으면 scene['duration']을 사용 = 사일런트 모드)
  2) 슬라이드 PNG → ImageClip + 살짝 줌인 효과
  3) 씬 사이 0.25s crossfade
  4) 트랙: TTS(있으면 우선) + BGM(audio/bgm.wav) duck mix
  5) 자막 SRT를 ffmpeg burn-in 으로 영상에 입힘 (선택)

CLI:
  python compose.py            # mode = 'tts' if audio/scene_*.mp3 다 있으면, 아니면 'silent'
  python compose.py --silent   # TTS 무시하고 슬라이드+BGM+자막만
"""
import argparse, os, subprocess, glob, math
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeAudioClip,
    concatenate_videoclips, concatenate_audioclips, ColorClip
)
from moviepy.video.fx.all import fadein, fadeout
from scenes import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(HERE, "slides")
AUDIO  = os.path.join(HERE, "audio")
OUT    = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 720
FPS  = 24


def measure_audio_durations():
    durations = []
    all_present = True
    for sc in SCENES:
        p = os.path.join(AUDIO, f"scene_{sc['id']:02d}.mp3")
        if os.path.exists(p) and os.path.getsize(p) > 1024:
            try:
                a = AudioFileClip(p)
                durations.append((sc, p, a.duration + 0.6))  # +0.6s tail for breathing
                a.close()
            except Exception as e:
                print(f"  WARN: cannot read {p}: {e}")
                durations.append((sc, None, sc["duration"]))
                all_present = False
        else:
            durations.append((sc, None, sc["duration"]))
            all_present = False
    return durations, all_present


def kenburns_clip(img_path, duration):
    """Slow zoom-in for cinematic feel."""
    clip = ImageClip(img_path).set_duration(duration)
    # subtle zoom 1.0 → 1.05
    def resize_factor(t):
        return 1.0 + 0.05 * (t / max(duration, 0.001))
    try:
        clip = clip.resize(resize_factor)
    except Exception:
        pass  # if resize without PIL OK fails, skip — static is fine
    return clip.set_fps(FPS)


def build_video(silent=False):
    print("== compose ==")
    triplets, all_audio_present = measure_audio_durations()
    use_tts = (not silent) and all_audio_present
    print(f"  TTS audio present: {all_audio_present}  →  use_tts = {use_tts}")

    # build video clips
    video_clips = []
    audio_segments = []
    cumulative = 0.0
    timeline = []
    for sc, audio_path, dur in triplets:
        slide_path = os.path.join(SLIDES, f"scene_{sc['id']:02d}.png")
        v = kenburns_clip(slide_path, dur)
        video_clips.append(v)
        # collect audio
        if use_tts and audio_path:
            a = AudioFileClip(audio_path)
            # pad with silence so audio length matches dur
            if a.duration < dur:
                from moviepy.audio.AudioClip import AudioClip
                # silent tail
                silent_clip = AudioClip(lambda t: 0, duration=(dur - a.duration), fps=44100)
                a = concatenate_audioclips([a, silent_clip])
            elif a.duration > dur:
                a = a.subclip(0, dur)
            audio_segments.append(a)
        timeline.append((sc["id"], cumulative, cumulative + dur, sc["narration"]))
        cumulative += dur

    print(f"  total clips: {len(video_clips)}  total duration: {cumulative:.1f}s ({int(cumulative//60)}:{int(cumulative%60):02d})")

    final_video = concatenate_videoclips(video_clips, method="compose")

    # build final audio
    final_audio = None
    if use_tts and audio_segments:
        narration = concatenate_audioclips(audio_segments)
        # mix with bgm if available
        bgm_path = os.path.join(AUDIO, "bgm.wav")
        if os.path.exists(bgm_path):
            try:
                bgm = AudioFileClip(bgm_path).volumex(0.18)
                if bgm.duration < narration.duration:
                    bgm = bgm.fx(lambda c: c.set_duration(narration.duration))
                bgm = bgm.subclip(0, narration.duration)
                final_audio = CompositeAudioClip([bgm, narration.volumex(1.0)])
            except Exception as e:
                print(f"  WARN: BGM mix failed: {e}")
                final_audio = narration
        else:
            final_audio = narration
    else:
        # silent mode → only BGM
        bgm_path = os.path.join(AUDIO, "bgm.wav")
        if os.path.exists(bgm_path):
            bgm = AudioFileClip(bgm_path).volumex(0.5)
            if bgm.duration < cumulative:
                # loop
                from moviepy.audio.fx.audio_loop import audio_loop
                bgm = audio_loop(bgm, duration=cumulative)
            else:
                bgm = bgm.subclip(0, cumulative)
            final_audio = bgm

    if final_audio is not None:
        final_video = final_video.set_audio(final_audio)

    out_mp4 = os.path.join(OUT, "AI_평균_책_깊이_10min.mp4")
    print(f"  rendering → {out_mp4}")
    final_video.write_videofile(
        out_mp4,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        bitrate="1800k",
        preset="ultrafast",
        threads=4,
        verbose=False,
        logger=None,
    )

    # build SRT with measured durations
    from srt_gen import make_srt
    srt_path = os.path.join(OUT, "subtitles.srt")
    make_srt([(sc, dur) for sc, _, dur in triplets], srt_path)

    return out_mp4, srt_path, cumulative


def burn_subtitles(in_mp4, srt_path, out_mp4, font_path):
    """Use ffmpeg subtitles filter to burn-in SRT (Korean)."""
    # ffmpeg subtitles filter requires the font file path & font name
    fontname = "NanumGothic"
    font_dir = os.path.dirname(font_path)
    style = (
        f"FontName={fontname},FontSize=22,PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H99000000,BackColour=&H00000000,"
        f"Outline=2,Shadow=0,Alignment=2,MarginV=80"
    )
    vf = f"subtitles={srt_path}:fontsdir={font_dir}:force_style='{style}'"
    cmd = [
        "ffmpeg", "-y", "-i", in_mp4, "-vf", vf,
        "-c:a", "copy", "-c:v", "libx264", "-preset", "medium",
        "-crf", "20", out_mp4,
    ]
    print("  burn:", " ".join(cmd[:8]), "...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mp4


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--silent", action="store_true",
                    help="ignore TTS, build silent slideshow + BGM only")
    ap.add_argument("--burn-subs", action="store_true",
                    help="burn-in Korean subtitles to a final MP4")
    args = ap.parse_args()
    out_mp4, srt, total = build_video(silent=args.silent)
    print(f"  done: {out_mp4}  {total:.1f}s")
    if args.burn_subs:
        font_path = os.path.join(HERE, "fonts", "NanumGothic.ttf")
        burned = os.path.join(OUT, "AI_평균_책_깊이_10min_subs.mp4")
        burn_subtitles(out_mp4, srt, burned, font_path)
        print(f"  burned: {burned}")
