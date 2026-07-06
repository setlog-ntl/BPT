"""쇼츠용 SRT 자막 생성"""
import os
from scenes_shorts import SCENES

def fmt(t):
    h = int(t//3600); m = int((t%3600)//60); s = int(t%60); ms = int((t-int(t))*1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def make_srt(triplets, out_path):
    """triplets: [(scene, audio_path, dur), ...]"""
    lines = []; t = 0.0
    for i, (sc, _, dur) in enumerate(triplets, start=1):
        text = sc["narration"] or sc.get("caption", "")
        lines.append(str(i))
        lines.append(f"{fmt(t)} --> {fmt(t + dur)}")
        lines.append(text)
        lines.append("")
        t += dur
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path
