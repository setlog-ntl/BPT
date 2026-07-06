"""쇼츠 영상 합성 — 1080x1920 30fps + ffmpeg"""
import os, subprocess, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except: pass
from scenes_shorts import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(HERE, "slides")
AUDIO  = os.path.join(HERE, "audio")
OUT    = os.path.join(HERE, "output")
TMP    = os.path.join(HERE, "tmp_render")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

W, H = 1080, 1920
FPS = 30


def ffprobe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path],
                       capture_output=True, text=True, errors="replace")
    return float(r.stdout.strip()) if r.stdout.strip() else 0.0


def measure():
    out = []
    for sc in SCENES:
        p = os.path.join(AUDIO, f"scene_{sc['id']:02d}.mp3")
        if os.path.exists(p) and os.path.getsize(p) > 1024:
            d = ffprobe_dur(p) + 0.3
            out.append((sc, p, d))
        else:
            out.append((sc, None, sc["duration"]))
    return out


def build_silent(triplets, out_path):
    list_file = os.path.join(TMP, "concat.txt")
    seg_paths = []
    for sc, _, dur in triplets:
        slide = os.path.join(SLIDES, f"scene_{sc['id']:02d}.png")
        seg = os.path.join(TMP, f"seg_{sc['id']:02d}.mp4")
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
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            print("seg fail:", (r.stderr or "")[-300:]); sys.exit(1)
        seg_paths.append(seg)
    with open(list_file, "w") as f:
        for p in seg_paths:
            f.write(f"file '{p}'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
           "-c", "copy", out_path]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print("concat fail:", (r.stderr or "")[-300:]); sys.exit(1)
    return out_path


def build_audio(triplets, bgm_path, out_audio):
    seg_wavs = []
    for sc, audio, dur in triplets:
        seg = os.path.join(TMP, f"audio_seg_{sc['id']:02d}.wav")
        if os.path.exists(seg) and os.path.getsize(seg) > 1024:
            seg_wavs.append(seg); continue
        if audio:
            cmd = ["ffmpeg", "-y", "-i", audio,
                   "-af", f"afade=t=in:st=0:d=0.05,apad=pad_dur={max(0.05,dur):.3f},"
                          f"atrim=end={dur:.3f},"
                          f"afade=t=out:st={max(0.0,dur-0.18):.3f}:d=0.18",
                   "-ar", "44100", "-ac", "2", seg]
        else:
            cmd = ["ffmpeg", "-y", "-f", "lavfi",
                   "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                   "-t", f"{dur:.3f}", seg]
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            print("audio seg fail:", (r.stderr or "")[-300:]); sys.exit(1)
        seg_wavs.append(seg)
    list_file = os.path.join(TMP, "audio_concat.txt")
    with open(list_file, "w") as f:
        for p in seg_wavs:
            f.write(f"file '{p}'\n")
    narr = os.path.join(TMP, "narration.wav")
    if not (os.path.exists(narr) and os.path.getsize(narr) > 1024):
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
                        "-c", "copy", narr], check=True, capture_output=True)
    has_n = any(t[1] for t in triplets)
    if has_n:
        cmd = ["ffmpeg", "-y", "-i", narr, "-i", bgm_path,
               "-filter_complex",
               "[0:a]highpass=f=80,equalizer=f=200:width_type=q:width=1.4:g=1.5,"
               "equalizer=f=3500:width_type=q:width=1.5:g=1.2,"
               "equalizer=f=6500:width_type=q:width=2:g=-2.5,"
               "acompressor=threshold=-18dB:ratio=2.8:attack=15:release=180:makeup=2.5,"
               "aresample=44100,volume=1.05[narr];"
               "[1:a]volume=0.20[bgm];"
               "[bgm][narr]sidechaincompress=threshold=0.06:ratio=8:attack=20:release=400[bgmd];"
               "[narr][bgmd]amix=inputs=2:duration=first:dropout_transition=2,"
               "loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
               "-map", "[aout]", out_audio]
    else:
        cmd = ["ffmpeg", "-y", "-i", bgm_path, "-af", "volume=0.6",
               "-t", f"{sum(t[2] for t in triplets):.3f}", out_audio]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print("mix fail:", (r.stderr or "")[-500:]); sys.exit(1)
    return out_audio


def burn_subs(in_mp4, srt, out_mp4):
    """Korean burn-in with safe path workaround"""
    import shutil, tempfile
    font_path = os.path.join(HERE, "fonts", "NanumGothic.ttf")
    tmp_dir = tempfile.mkdtemp()
    safe_srt = os.path.join(tmp_dir, "subs.srt")
    safe_in = os.path.join(tmp_dir, "in.mp4")
    safe_out = os.path.join(tmp_dir, "out.mp4")
    safe_fonts = os.path.join(tmp_dir, "fonts")
    os.makedirs(safe_fonts, exist_ok=True)
    shutil.copy(srt, safe_srt)
    shutil.copy(in_mp4, safe_in)
    shutil.copy(font_path, os.path.join(safe_fonts, "NanumGothic.ttf"))
    srt_filt = safe_srt.replace("\\", "/").replace(":", "\\:")
    fonts_filt = safe_fonts.replace("\\", "/").replace(":", "\\:")
    style = ("FontName=NanumGothic,FontSize=20,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H99000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=200")
    vf = f"subtitles='{srt_filt}':fontsdir='{fonts_filt}':force_style='{style}'"
    cmd = ["ffmpeg", "-y", "-i", safe_in, "-vf", vf,
           "-c:a", "copy", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24", safe_out]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print("burn fail:", (r.stderr or "")[-500:]); sys.exit(1)
    shutil.copy(safe_out, out_mp4)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return out_mp4


def main():
    print("[1] measure")
    triplets = measure()
    total = sum(t[2] for t in triplets)
    has_n = any(t[1] for t in triplets)
    print(f"  {len(triplets)} scenes total {total:.1f}s; TTS={has_n}")

    print("[2] build silent video")
    silent = os.path.join(TMP, "silent.mp4")
    if not (os.path.exists(silent) and os.path.getsize(silent) > 1024):
        build_silent(triplets, silent)
    print(f"  -> {silent}")

    print("[3] build audio")
    bgm = os.path.join(AUDIO, "bgm.wav")
    aud = os.path.join(TMP, "audio.wav")
    if not (os.path.exists(aud) and os.path.getsize(aud) > 1024):
        build_audio(triplets, bgm, aud)
    print(f"  -> {aud}")

    print("[4] mux")
    final = os.path.join(OUT, "shorts_pre.mp4")
    cmd = ["ffmpeg", "-y", "-i", silent, "-i", aud, "-map", "0:v", "-map", "1:a",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", final]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print("mux fail:", (r.stderr or "")[-300:]); sys.exit(1)
    print(f"  -> {final}")

    print("[5] SRT")
    from srt_shorts import make_srt
    srt = os.path.join(OUT, "shorts.srt")
    make_srt(triplets, srt)
    print(f"  -> {srt}")

    print("[6] burn subtitles")
    final_subs = os.path.join(OUT, "shorts_final.mp4")
    burn_subs(final, srt, final_subs)
    print(f"  -> {final_subs}")
    print("\nDONE.")


if __name__ == "__main__":
    main()
