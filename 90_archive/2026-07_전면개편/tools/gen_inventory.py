# -*- coding: utf-8 -*-
"""PHASE 0 전수 인벤토리 생성기 — _migration/00_인벤토리.md 출력"""
import os
import datetime

ROOT = r"C:\Dev\bizpt"
OUT = os.path.join(ROOT, "_migration", "00_인벤토리.md")
EXCLUDE_DIRS = {".git"}
BIG_FILE_MB = 5

def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}B"
        n /= 1024

def main():
    records = []  # (relpath, size, mtime)
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                st = os.stat(fp)
            except OSError:
                continue
            rel = os.path.relpath(fp, ROOT)
            records.append((rel, st.st_size, st.st_mtime))

    records.sort(key=lambda r: r[0].lower())
    total_size = sum(r[1] for r in records)

    # 최상위 그룹핑
    groups = {}
    for rel, size, mtime in records:
        top = rel.split(os.sep)[0] if os.sep in rel else "(루트 직속)"
        g = groups.setdefault(top, {"count": 0, "size": 0, "mtime": 0, "files": []})
        g["count"] += 1
        g["size"] += size
        g["mtime"] = max(g["mtime"], mtime)
        g["files"].append((rel, size, mtime))

    big_files = [(r, s, m) for r, s, m in records if s >= BIG_FILE_MB * 1024 * 1024]
    big_files.sort(key=lambda r: -r[1])

    # 잔해/백업 후보
    debris = []
    for rel, size, mtime in records:
        base = os.path.basename(rel).lower()
        top = rel.split(os.sep)[0]
        is_root = os.sep not in rel
        if (".bak" in base or base == "testnote.nd"
                or (is_root and base.startswith("check_") and base.endswith(".jpg"))
                or (is_root and base.endswith((".png", ".zip")))
                or (is_root and base.startswith("page-"))):
            debris.append((rel, size, mtime))

    ts = lambda m: datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d")
    lines = []
    lines.append("# PHASE 0 — 전수 인벤토리")
    lines.append("")
    lines.append(f"> 생성: {datetime.date.today().isoformat()} · 도구: `_migration/tools/gen_inventory.py` · `.git` 제외")
    lines.append("")
    lines.append(f"**총계: 파일 {len(records):,}개 · {human(total_size)}**")
    lines.append("")
    lines.append("## 1. 최상위 구역 요약")
    lines.append("")
    lines.append("| 구역 | 파일 수 | 총 크기 | 최근 수정 |")
    lines.append("|---|---:|---:|---|")
    for top in sorted(groups, key=lambda t: -groups[t]["size"]):
        g = groups[top]
        lines.append(f"| `{top}` | {g['count']} | {human(g['size'])} | {ts(g['mtime'])} |")
    lines.append("")
    lines.append(f"## 2. 대용량 파일 (≥{BIG_FILE_MB}MB) — git 이력 부담·이동 최소화 검토 대상")
    lines.append("")
    lines.append("| 파일 | 크기 | 수정일 |")
    lines.append("|---|---:|---|")
    for rel, size, mtime in big_files:
        lines.append(f"| `{rel}` | {human(size)} | {ts(mtime)} |")
    lines.append("")
    lines.append("## 3. 잔해·백업 후보 (90_archive 이동 검토 대상)")
    lines.append("")
    lines.append("| 파일 | 크기 | 수정일 |")
    lines.append("|---|---:|---|")
    for rel, size, mtime in sorted(debris):
        lines.append(f"| `{rel}` | {human(size)} | {ts(mtime)} |")
    lines.append("")
    lines.append("## 4. 전체 파일 목록 (구역별)")
    lines.append("")
    for top in sorted(groups, key=str.lower):
        g = groups[top]
        lines.append(f"<details><summary><b>{top}</b> — {g['count']}개 · {human(g['size'])}</summary>")
        lines.append("")
        lines.append("| 파일 | 크기 | 수정일 |")
        lines.append("|---|---:|---|")
        for rel, size, mtime in g["files"]:
            lines.append(f"| `{rel}` | {human(size)} | {ts(mtime)} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"OK: {OUT} / files={len(records)} size={human(total_size)} big={len(big_files)} debris={len(debris)}")

if __name__ == "__main__":
    main()
