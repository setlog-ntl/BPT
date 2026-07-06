# -*- coding: utf-8 -*-
"""뷰트랩 단어 대시보드 빌더 v3 - 카테고리 지원."""
import csv, json, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "대시보드_템플릿.html"
OUTPUT = ROOT / "대시보드.html"

def safe_int(s, default=0):
    if s is None: return default
    try:
        return int(str(s).replace(",", "").replace('"', "").strip() or default)
    except: return default

def load_cumulative(p):
    fp = p / "누적_데이터.csv"
    if not fp.exists(): return []
    with open(fp, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_videos(csv_path):
    if not csv_path.exists(): return []
    out = []
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append({
                "rank": safe_int(r.get("순번", 0)),
                "duration": r.get("영상길이", ""),
                "title": r.get("제목", ""),
                "views": safe_int(r.get("조회수", 0)),
                "subscribers": safe_int(r.get("구독자", 0)),
                "channel": r.get("채널명", ""),
                "contribution": r.get("기여도", ""),
                "performance": r.get("성과도", ""),
                "exposure": r.get("노출확률", ""),
                "total_videos": safe_int(r.get("총영상수", 0)),
                "published_at": r.get("게시일", ""),
                "thumbnail": r.get("썸네일URL", ""),
            })
    return out

def scan_keyword(entry, category):
    cumulative = load_cumulative(entry)
    captures = []
    for d in sorted(entry.iterdir()):
        if not d.is_dir(): continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", d.name): continue
        captures.append({
            "date": d.name,
            "videos_all": load_videos(d / "상위영상목록.csv"),
            "videos_filtered": load_videos(d / "필터적용_영상목록.csv"),
        })
    latest = cumulative[-1] if cumulative else {}
    return {
        "name": entry.name,
        "category": category,
        "captures_count": len(cumulative),
        "first_capture": cumulative[0]["캡처일"] if cumulative else "",
        "last_capture": cumulative[-1]["캡처일"] if cumulative else "",
        "latest_total_videos": safe_int(latest.get("총영상수", 0)),
        "latest_views_sum": safe_int(latest.get("조회수합계", 0)),
        "latest_views_avg": safe_int(latest.get("조회수평균", 0)),
        "latest_views_median": safe_int(latest.get("조회수중앙값", 0)),
        "latest_subs_sum": safe_int(latest.get("구독자합계", 0)),
        "latest_subs_avg": safe_int(latest.get("구독자평균", 0)),
        "latest_subs_median": safe_int(latest.get("구독자중앙값", 0)),
        "latest_likes_sum": safe_int(latest.get("좋아요합계", 0)),
        "latest_likes_avg": safe_int(latest.get("좋아요평균", 0)),
        "latest_likes_median": safe_int(latest.get("좋아요중앙값", 0)),
        "filter_passed": safe_int(latest.get("필터통과수", 0)),
        "cumulative": cumulative,
        "captures": captures,
    }

def scan_keywords():
    keywords = []
    for cat_dir in sorted(ROOT.iterdir()):
        if not cat_dir.is_dir(): continue
        if re.match(r"^[A-Z]_", cat_dir.name):
            cat_label = cat_dir.name.replace("_", " ", 1)
            for kw_dir in sorted(cat_dir.iterdir()):
                if not kw_dir.is_dir(): continue
                if not (kw_dir / "누적_데이터.csv").exists(): continue
                keywords.append(scan_keyword(kw_dir, cat_label))
        elif (cat_dir / "누적_데이터.csv").exists():
            keywords.append(scan_keyword(cat_dir, "기타"))
    return keywords

def build():
    if not TEMPLATE.exists():
        print("[ERROR] 템플릿이 없습니다:", TEMPLATE); return
    keywords = scan_keywords()
    template = TEMPLATE.read_text(encoding="utf-8")
    data_json = json.dumps(keywords, ensure_ascii=False)
    html = template.replace("__DATA_JSON__", data_json)
    html = html.replace("__BUILD_TIME__", datetime.now().strftime("%Y-%m-%d %H:%M"))
    OUTPUT.write_text(html, encoding="utf-8")
    print("[OK] 대시보드 생성:", OUTPUT)
    cats = {}
    for k in keywords:
        cats.setdefault(k["category"], []).append(k["name"])
    print(f"     카테고리 {len(cats)}개, 키워드 {len(keywords)}개")
    for cat, names in cats.items():
        print(f"     - {cat}: {', '.join(names)}")

if __name__ == "__main__":
    build()
