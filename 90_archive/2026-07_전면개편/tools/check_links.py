# -*- coding: utf-8 -*-
"""PHASE 0 링크 그래프 추출·유효/사망 판정기 — _migration/01_링크그래프.md 출력
저장소 내 모든 html/md의 상대경로 링크를 추출해 대상 존재 여부를 판정한다.
"""
import os
import re
import urllib.parse
import datetime

ROOT = r"C:\Dev\bizpt"
OUT = os.path.join(ROOT, "_migration", "01_링크그래프.md")
EXCLUDE_DIRS = {".git", "node_modules"}

HTML_LINK = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
MD_LINK = re.compile(r"""\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+["'][^)]*["'])?\s*\)""")
SKIP_PREFIX = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "#", "//")


def collect_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f.lower().endswith((".html", ".md", ".markdown", ".htm")):
                out.append(os.path.join(dirpath, f))
    return sorted(out, key=str.lower)


def extract_links(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    links = []
    lower = path.lower()
    if lower.endswith((".html", ".htm")):
        links += HTML_LINK.findall(text)
        links += MD_LINK.findall(text)  # html 내 md 표기 거의 없음, 무해
    else:
        links += MD_LINK.findall(text)
        links += HTML_LINK.findall(text)  # md 내 <a href> / <img src>
    return links


def is_placeholder(t):
    """예시·템플릿 변수 등 실링크가 아닌 의사(pseudo) 링크 판정"""
    return ("${" in t or "<" in t or ">" in t or "..." in t or "*" in t
            or t in ("URL", "url", "#", "경로", "파일명")
            or "NNN" in t or "YYYY" in t or "<base" in t)


def resolve(src_file, target):
    t = target.strip()
    if not t or t.startswith(SKIP_PREFIX):
        return None
    t = t.split("#", 1)[0].split("?", 1)[0]
    if not t:
        return None
    t = urllib.parse.unquote(t)
    if t.startswith("/"):
        cand = os.path.normpath(os.path.join(ROOT, t.lstrip("/")))
    else:
        cand = os.path.normpath(os.path.join(os.path.dirname(src_file), t))
    return cand


def main():
    files = collect_files()
    rows = []  # (src_rel, raw_target, resolved_rel, ok)
    pseudo = []  # 플레이스홀더 의사 링크 (수리 불필요)
    for fp in files:
        seen = set()
        for raw in extract_links(fp):
            if raw.strip() and is_placeholder(raw.strip()):
                key = (fp, raw)
                if key not in seen:
                    seen.add(key)
                    pseudo.append((os.path.relpath(fp, ROOT), raw))
                continue
            cand = resolve(fp, raw)
            if cand is None:
                continue
            key = (fp, raw)
            if key in seen:
                continue
            seen.add(key)
            ok = os.path.exists(cand)
            rows.append((os.path.relpath(fp, ROOT), raw, os.path.relpath(cand, ROOT), ok))

    dead = [r for r in rows if not r[3]]
    by_src = {}
    for r in rows:
        by_src.setdefault(r[0], []).append(r)

    def is_hub(rel):
        b = os.path.basename(rel)
        return (rel == "index.html" or b.startswith("통합_") or "허브" in b
                or b.startswith("_댓글분석") or b in ("README.md", "CLAUDE.md"))

    lines = []
    lines.append("# PHASE 0 — 링크 그래프 (유효/사망 판정)")
    lines.append("")
    lines.append(f"> 생성: {datetime.date.today().isoformat()} · 도구: `_migration/tools/check_links.py`")
    lines.append("> 대상: 저장소 내 전체 html/md의 상대경로 링크 (외부 URL·앵커 제외). 이 판정이 PHASE 4 이동/수리의 근거다.")
    lines.append("")
    lines.append(f"**전체 통계: 스캔 파일 {len(files)}개 · 내부 링크 {len(rows)}건 · 유효 {len(rows)-len(dead)}건 · 사망 {len(dead)}건**")
    lines.append("")
    lines.append("## 1. 사망 링크 전수 목록 (수리 의무 대상)")
    lines.append("")
    lines.append("| 원본 파일 | 링크 원문 | 해석된 경로 |")
    lines.append("|---|---|---|")
    for src, raw, res, ok in dead:
        lines.append(f"| `{src}` | `{raw}` | `{res}` |")
    lines.append("")
    lines.append("## 2. index.html 외부 참조 전수 (SPA — 하드 룰 1)")
    lines.append("")
    lines.append("| 링크 원문 | 해석된 경로 | 판정 |")
    lines.append("|---|---|---|")
    for src, raw, res, ok in by_src.get("index.html", []):
        lines.append(f"| `{raw}` | `{res}` | {'✅ 유효' if ok else '❌ 사망'} |")
    lines.append("")
    lines.append("## 3. 파일별 요약 (링크 보유 파일 전체)")
    lines.append("")
    lines.append("| 파일 | 링크 수 | 사망 수 | 허브 여부 |")
    lines.append("|---|---:|---:|---|")
    for src in sorted(by_src, key=str.lower):
        rs = by_src[src]
        d = sum(1 for r in rs if not r[3])
        lines.append(f"| `{src}` | {len(rs)} | {d} | {'🔗 허브' if is_hub(src) else ''} |")
    lines.append("")
    lines.append("## 4. 허브 파일 상세 (index.html 외 허브류)")
    lines.append("")
    for src in sorted(by_src, key=str.lower):
        if not is_hub(src) or src == "index.html":
            continue
        rs = by_src[src]
        d = sum(1 for r in rs if not r[3])
        lines.append(f"<details><summary><b>{src}</b> — {len(rs)}건 (사망 {d})</summary>")
        lines.append("")
        lines.append("| 링크 원문 | 판정 |")
        lines.append("|---|---|")
        for _, raw, res, ok in rs:
            lines.append(f"| `{raw}` | {'✅' if ok else '❌ → ' + res} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"OK: {OUT} / scanned={len(files)} links={len(rows)} dead={len(dead)}")
    print("DEAD SAMPLE (max 30):")
    for src, raw, res, ok in dead[:30]:
        print(f"  {src} -> {raw}")

if __name__ == "__main__":
    main()
