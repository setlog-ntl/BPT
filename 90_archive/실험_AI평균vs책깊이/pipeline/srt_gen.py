"""
씬별 노출 시간으로 SRT 자막 파일 생성 (한국어)
narration이 있는 경우는 그것을, 없으면 caption을 자막으로 사용
"""
import os
from scenes import SCENES

def fmt_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

def make_srt(scenes_with_durations, out_path):
    """scenes_with_durations: list of (scene_dict, audio_duration_sec)"""
    lines = []
    t = 0.0
    for i, (sc, dur) in enumerate(scenes_with_durations, start=1):
        text = sc["narration"] or sc.get("caption", "")
        start = t
        end = t + dur
        lines.append(str(i))
        lines.append(f"{fmt_time(start)} --> {fmt_time(end)}")
        lines.append(text)
        lines.append("")
        t = end
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path

if __name__ == "__main__":
    # if no audio yet, use planned durations
    pairs = [(s, s["duration"]) for s in SCENES]
    out = os.path.join(os.path.dirname(__file__), "output", "subtitles.srt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    make_srt(pairs, out)
    print("SRT:", out)
