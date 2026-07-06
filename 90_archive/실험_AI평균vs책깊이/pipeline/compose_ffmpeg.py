"""
ffmpeg 기반 영상 합성기 (moviepy 보다 10x 빠름)

흐름:
1) 씬별 (slide.png + duration) → 단일 MP4로 인코드 (concat 데모더용 input.txt 생성)
2) 모든 씬 concat
3) BGM(+TTS 있으면 narration) 합성
4) (선택) 자막 burn-in
"""
import os, subprocess, argparse, sys, json
from scenes import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(HERE, "slides")
AUDIO  = os.path.join(HERE, "audio")
OUT    = os.path.join(HERE, "output")
TMP    = os.path.join(HERE, "tmp_render")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

W, H = 1280, 720
FPS  = 24


def ffprobe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return float(r.stdout.strip()) if r.stdout.strip() else 0.0


def measure_durations():
    triplets = []
    all_present = True
    for sc in SCENES:
        p = os.path.join(AUDIO, f"scene_{sc['id']:02d}.mp3")
        if os.path.exists(p) and os.path.getsize(p) > 1024:
            d = ffprobe_duration(p) + 0.4   # tail breathing
            triplets.append((sc, p, d))
        else:
            triplets.append((sc, None, sc["duration"]))
            all_present = False
    return triplets, all_present


def build_silent_video(triplets, out_path, with_zoom=False):
    """Per-scene mp4 → concat. Static frames (no zoom for max speed in sandbox)."""
    list_file = os.path.join(TMP, "concat_list.txt")
    seg_paths = []
    for sc, _, dur in triplets:
        slide  = os.path.join(SLIDES, f"scene_{sc['id']:02d}.png")
        seg    = os.path.join(TMP, f"seg_{sc['id']:02d}.mp4")
        if os.path.exists(seg) and os.path.getsize(seg) > 1024:
            seg_paths.append(seg); continue
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", slide,
            "-t", f"{dur:.3f}",
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                   f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-r", str(FPS),
            "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage",
            "-pix_fmt", "yuv420p", "-an", seg
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print("ffmpeg seg fail:", r.stderr[-400:])
            sys.exit(1)
        seg_paths.append(seg)
    # write concat list
    with open(list_file, "w") as f:
        for p in seg_paths:
            f.write(f"file '{p}'\n")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("concat fail:", r.stderr[-500:])
        sys.exit(1)
    return out_path


def mux_audio(video_path, narration_paths, bgm_path, out_path, narration_volume=1.0, bgm_volume=0.18, total_dur=None):
    """Build final audio: narration concat (with silence padding per scene) + bgm sidechain"""
    has_narration = any(p is not None for p in narration_paths)
    inputs = ["-i", video_path]
    filter_parts = []
    audio_idx = 1

    if has_narration:
        # Build concatenated narration with silent gaps so each scene lines up with its slide.
        # We'll generate a single narration.wav using ffmpeg's adelay+amix logic — but simplest:
        # for each scene, use the audio file or silence pad to dur, then concat.
        # First, build per-scene audio segments as wav.
        seg_wavs = []
        for i, (sc, audio, dur) in enumerate(zip(narration_paths_data, narration_paths_data, narration_paths_data)):
            pass  # placeholder — redone below
        raise NotImplementedError("see compose_ffmpeg_v2.py")
    else:
        # bgm only
        inputs += ["-stream_loop", "-1", "-i", bgm_path]
        filter_parts = [
            f"[1:a]volume={bgm_volume}[bgm]"
        ]
        cmd = (["ffmpeg", "-y"] + inputs +
               ["-filter_complex", ";".join(filter_parts),
                "-map", "0:v", "-map", "[bgm]",
                "-shortest",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k",
                out_path])
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print("mux fail:", r.stderr[-500:])
            sys.exit(1)
        return out_path


def build_audio_track(triplets, bgm_path, out_audio):
    """Construct full narration+bgm as one wav: per scene use narration or silence of dur length."""
    # 1) build per-scene wav
    seg_wavs = []
    for sc, audio, dur in triplets:
        seg = os.path.join(TMP, f"audio_seg_{sc['id']:02d}.wav")
        if os.path.exists(seg) and os.path.getsize(seg) > 1024:
            seg_wavs.append(seg); continue
        if audio:
            # decode mp3, pad to dur with silence at end if shorter
            cmd = [
                "ffmpeg", "-y", "-i", audio,
                "-af", f"afade=t=in:st=0:d=0.05,apad=pad_dur={max(0.05, dur):.3f},atrim=end={dur:.3f},afade=t=out:st={max(0.0, dur-0.18):.3f}:d=0.18,volume=1.0",
                "-ar", "44100", "-ac", "2", seg
            ]
        else:
            # silence of dur
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
                "-t", f"{dur:.3f}", seg
            ]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print("audio seg fail:", r.stderr[-400:]); sys.exit(1)
        seg_wavs.append(seg)
    # 2) concat narrations
    list_file = os.path.join(TMP, "audio_concat.txt")
    with open(list_file, "w") as f:
        for p in seg_wavs:
            f.write(f"file '{p}'\n")
    narr = os.path.join(TMP, "narration_full.wav")
    if not (os.path.exists(narr) and os.path.getsize(narr) > 1024):
      subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
         "-c", "copy", narr], check=True, capture_output=True)
    # 3) mix with BGM
    has_narration = any(t[1] for t in triplets)
    if has_narration:
        # narration foreground, bgm under
        cmd = [
            "ffmpeg", "-y", "-i", narr, "-i", bgm_path,
            "-filter_complex",
            # narration mastering: HPF + de-ess + compressor + slight reverb tail + LUFS norm
            "[0:a]highpass=f=80,equalizer=f=200:width_type=q:width=1.4:g=1,equalizer=f=3500:width_type=q:width=1.5:g=1.2,equalizer=f=6500:width_type=q:width=2:g=-2.5,acompressor=threshold=-18dB:ratio=2.8:attack=15:release=180:makeup=2.5,aresample=44100,volume=1.05[narr_master];"
            # BGM: lower volume + sidechain duck by narration
            "[1:a]volume=0.22[bgm];"
            "[bgm][narr_master]sidechaincompress=threshold=0.06:ratio=8:attack=20:release=400[bgm_duck];"
            "[narr_master][bgm_duck]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
            "-map", "[aout]", out_audio
        ]
    else:
        # bgm only at full
        cmd = [
            "ffmpeg", "-y", "-i", bgm_path,
            "-af", "volume=0.6",
            "-t", f"{sum(t[2] for t in triplets):.3f}",
            out_audio
        ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("audio mix fail:", r.stderr[-500:]); sys.exit(1)
    return out_audio


def burn_subtitles(in_mp4, srt_path, out_mp4):
    """Burn-in subtitles. Workaround for Windows path-with-Korean ffmpeg subtitles filter."""
    font_path = os.path.join(HERE, "fonts", "NanumGothic.ttf")
    fontname = "NanumGothic"
    font_dir = os.path.dirname(font_path)
    style = (f"FontName={fontname},FontSize=18,PrimaryColour=&H00FFFFFF,"
             f"OutlineColour=&H99000000,BackColour=&H00000000,"
             f"Outline=2,Shadow=0,Alignment=2,MarginV=60")

    # Workaround: copy SRT to a path with no special chars (system temp), then burn-in
    import shutil, tempfile
    tmp_dir = tempfile.mkdtemp()
    safe_srt   = os.path.join(tmp_dir, "subs.srt")
    safe_in    = os.path.join(tmp_dir, "in.mp4")
    safe_out   = os.path.join(tmp_dir, "out.mp4")
    safe_fonts = os.path.join(tmp_dir, "fonts")
    os.makedirs(safe_fonts, exist_ok=True)
    shutil.copy(srt_path, safe_srt)
    shutil.copy(in_mp4, safe_in)
    shutil.copy(font_path, os.path.join(safe_fonts, "NanumGothic.ttf"))

    # forward-slash, escape-safe path for filter
    srt_filter = safe_srt.replace("\\", "/").replace(":", "\\:")
    fonts_filter = safe_fonts.replace("\\", "/").replace(":", "\\:")
    vf = f"subtitles='{srt_filter}':fontsdir='{fonts_filter}':force_style='{style}'"

    cmd = ["ffmpeg", "-y", "-i", safe_in, "-vf", vf,
           "-c:a", "copy", "-c:v", "libx264", "-preset", "ultrafast",
           "-crf", "26", safe_out]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("burn fail:", (r.stderr or "")[-500:])
        sys.exit(1)
    shutil.copy(safe_out, out_mp4)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return out_mp4



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--silent", action="store_true")
    ap.add_argument("--no-burn", action="store_true")
    args = ap.parse_args()

    print("[1] measuring scene durations...")
    triplets, all_present = measure_durations()
    if args.silent:
        triplets = [(s, None, d) for s, _, d in triplets]
        all_present = False
    total = sum(t[2] for t in triplets)
    print(f"    {len(triplets)} scenes, total {total:.1f}s ({int(total//60)}:{int(total%60):02d})")
    print(f"    TTS audio present: {all_present}")

    print("[2] building silent video segments...")
    silent_video = os.path.join(TMP, "silent.mp4")
    if os.path.exists(silent_video) and os.path.getsize(silent_video) > 1024:
        print("    [cached] silent.mp4 exists, skipping build")
    else:
        build_silent_video(triplets, silent_video)
    print(f"    -> {silent_video}  size={os.path.getsize(silent_video)/1024/1024:.1f}MB")

    print("[3] building audio track (narration + bgm)...")
    bgm_path = os.path.join(AUDIO, "bgm.wav")
    final_audio = os.path.join(TMP, "final_audio.aac")
    final_audio_wav = os.path.join(TMP, "final_audio.wav")
    if os.path.exists(final_audio_wav) and os.path.getsize(final_audio_wav) > 1024:
        print("    [cached] final_audio.wav exists")
    else:
        build_audio_track(triplets, bgm_path, final_audio_wav)
    print(f"    -> {final_audio_wav}")

    print("[4] muxing video + audio...")
    final_mp4 = os.path.join(OUT, "AI_평균_책_깊이_10min.mp4")
    cmd = ["ffmpeg", "-y", "-i", silent_video, "-i", final_audio_wav,
           "-map", "0:v", "-map", "1:a",
           "-c:v", "copy",
           "-c:a", "aac", "-b:a", "160k",
           "-shortest", final_mp4]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("mux fail:", r.stderr[-500:]); sys.exit(1)
    print(f"    -> {final_mp4}  size={os.path.getsize(final_mp4)/1024/1024:.1f}MB")

    print("[5] writing SRT subtitles...")
    from srt_gen import make_srt
    srt_path = os.path.join(OUT, "subtitles.srt")
    make_srt([(s, d) for s, _, d in triplets], srt_path)
    print(f"    -> {srt_path}")

    if not args.no_burn:
        print("[6] burning Korean subtitles into final video...")
        burned = os.path.join(OUT, "AI_평균_책_깊이_10min_subs.mp4")
        burn_subtitles(final_mp4, srt_path, burned)
        print(f"    -> {burned}  size={os.path.getsize(burned)/1024/1024:.1f}MB")

    print("\nDONE.")


if __name__ == "__main__":
    main()
