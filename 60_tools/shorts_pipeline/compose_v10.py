"""V10 쇼츠 합성 — 18씬 + AI 이미지 + Edge TTS"""
import os, subprocess, sys, shutil, tempfile
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except: pass
from scenes_shorts_v10 import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(HERE, "slides_v10")
AUDIO = os.path.join(HERE, "audio_v10")
OUT = os.path.join(HERE, "output_v10")
TMP = os.path.join(HERE, "tmp_v10")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30


def ffd(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", p],
                       capture_output=True, text=True, errors="replace")
    return float(r.stdout.strip()) if r.stdout.strip() else 0.0


def measure():
    out = []
    for sc in SCENES:
        p = os.path.join(AUDIO, f"scene_{sc['id']:02d}.mp3")
        if os.path.exists(p) and os.path.getsize(p) > 1024:
            out.append((sc, p, ffd(p) + 0.3))
        else:
            out.append((sc, None, 3.0))
    return out


def build_silent(triplets):
    paths = []
    list_file = os.path.join(TMP, "concat.txt")
    for sc, _, dur in triplets:
        slide = os.path.join(SLIDES, f"scene_{sc['id']:02d}.png")
        seg = os.path.join(TMP, f"seg_{sc['id']:02d}.mp4")
        if os.path.exists(seg) and os.path.getsize(seg) > 1024:
            paths.append(seg); continue
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", slide, "-t", f"{dur:.3f}",
               "-vf", f"scale={W}:{H},format=yuv420p", "-r", str(FPS),
               "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage",
               "-pix_fmt", "yuv420p", "-an", seg]
        subprocess.run(cmd, capture_output=True, text=True, errors="replace", check=True)
        paths.append(seg)
    with open(list_file, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    silent = os.path.join(TMP, "silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
                    "-c", "copy", silent], check=True, capture_output=True)
    return silent


def build_audio(triplets):
    seg_wavs = []
    for sc, audio, dur in triplets:
        seg = os.path.join(TMP, f"audio_seg_{sc['id']:02d}.wav")
        if os.path.exists(seg) and os.path.getsize(seg) > 1024:
            seg_wavs.append(seg); continue
        if audio:
            cmd = ["ffmpeg", "-y", "-i", audio,
                   "-af", f"afade=t=in:st=0:d=0.05,apad=pad_dur={dur:.3f},"
                          f"atrim=end={dur:.3f},"
                          f"afade=t=out:st={max(0,dur-0.18):.3f}:d=0.18",
                   "-ar", "44100", "-ac", "2", seg]
        else:
            cmd = ["ffmpeg", "-y", "-f", "lavfi",
                   "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                   "-t", f"{dur:.3f}", seg]
        subprocess.run(cmd, capture_output=True, text=True, errors="replace", check=True)
        seg_wavs.append(seg)
    list_file = os.path.join(TMP, "audio_concat.txt")
    with open(list_file, "w") as f:
        for p in seg_wavs:
            f.write(f"file '{p}'\n")
    narr = os.path.join(TMP, "narr.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
                    "-c", "copy", narr], check=True, capture_output=True)

    bgm = os.path.join(AUDIO, "bgm.wav")
    final = os.path.join(TMP, "audio_final.wav")
    cmd = ["ffmpeg", "-y", "-i", narr, "-i", bgm,
           "-filter_complex",
           "[0:a]highpass=f=80,equalizer=f=200:width_type=q:width=1.4:g=1.5,"
           "equalizer=f=3500:width_type=q:width=1.5:g=1.2,"
           "equalizer=f=6500:width_type=q:width=2:g=-2.5,"
           "acompressor=threshold=-18dB:ratio=2.8:attack=15:release=180:makeup=2.5,"
           "volume=1.05[narr];"
           "[1:a]volume=0.20[bgm];"
           "[bgm][narr]sidechaincompress=threshold=0.06:ratio=8:attack=20:release=400[bgmd];"
           "[narr][bgmd]amix=inputs=2:duration=first:dropout_transition=2,"
           "loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
           "-map", "[aout]", final]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print("audio mix fail:", (r.stderr or "")[-500:]); sys.exit(1)
    return final


def make_srt(triplets):
    def fmt(t):
        h = int(t//3600); m = int((t%3600)//60); s = int(t%60); ms = int((t-int(t))*1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    lines = []; t = 0
    for i, (sc, _, dur) in enumerate(triplets, start=1):
        lines.append(str(i))
        lines.append(f"{fmt(t)} --> {fmt(t+dur)}")
        lines.append(sc["narration"])
        lines.append("")
        t += dur
    p = os.path.join(OUT, "v10.srt")
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    return p


def burn(in_mp4, srt, out):
    font_path = os.path.join(HERE, "fonts", "NanumGothic.ttf")
    tmp = tempfile.mkdtemp()
    shutil.copy(srt, os.path.join(tmp, "s.srt"))
    shutil.copy(in_mp4, os.path.join(tmp, "i.mp4"))
    fd = os.path.join(tmp, "f"); os.makedirs(fd, exist_ok=True)
    shutil.copy(font_path, os.path.join(fd, "NanumGothic.ttf"))
    srtf = os.path.join(tmp, "s.srt").replace("\\", "/").replace(":", "\\:")
    fdf = fd.replace("\\", "/").replace(":", "\\:")
    style = ("FontName=NanumGothic,FontSize=20,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H99000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=180")
    vf = f"subtitles='{srtf}':fontsdir='{fdf}':force_style='{style}'"
    o2 = os.path.join(tmp, "out.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-i", os.path.join(tmp, "i.mp4"), "-vf", vf,
                        "-c:a", "copy", "-c:v", "libx264", "-preset", "ultrafast",
                        "-crf", "24", o2],
                       capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print("burn fail:", (r.stderr or "")[-500:]); sys.exit(1)
    shutil.copy(o2, out)
    shutil.rmtree(tmp, ignore_errors=True)


def main():
    triplets = measure()
    total = sum(t[2] for t in triplets)
    print(f"  {len(triplets)} scenes total {total:.1f}s")
    print("[1] silent")
    silent = build_silent(triplets)
    print("[2] audio")
    audio = build_audio(triplets)
    print("[3] mux")
    pre = os.path.join(OUT, "v10_pre.mp4")
    subprocess.run(["ffmpeg", "-y", "-i", silent, "-i", audio,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", pre],
                   check=True, capture_output=True)
    print("[4] srt")
    srt = make_srt(triplets)
    print("[5] burn")
    final = os.path.join(OUT, "v10_final.mp4")
    burn(pre, srt, final)
    print(f"DONE: {final}")


if __name__ == "__main__":
    main()
