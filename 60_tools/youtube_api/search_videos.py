# -*- coding: utf-8 -*-
"""S1 수요·기회 스코어 원료 — 키워드 검색 상위 영상 수집
사용: python search_videos.py "<키워드>" [--max 15] [--order viewCount|relevance] [--days 365] [--region KR]
출력: 20_research/keywords/api_<키워드>_<날짜>.json + .md
비용: search.list = 100 units/호출 (비쌈 — 하루 상한 유의, README 쿼터 규칙)
"""
import sys, json, io, datetime, argparse
import yt_common as Y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("--max", type=int, default=15)
    ap.add_argument("--order", default="relevance", choices=["relevance", "viewCount", "date"])
    ap.add_argument("--days", type=int, default=0, help="최근 N일 이내로 제한 (0=전체)")
    ap.add_argument("--region", default="KR")
    a = ap.parse_args()

    params = {"part": "snippet", "q": a.keyword, "type": "video", "maxResults": min(a.max, 50),
              "order": a.order, "regionCode": a.region, "relevanceLanguage": "ko"}
    if a.days:
        after = (datetime.datetime.utcnow() - datetime.timedelta(days=a.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
        params["publishedAfter"] = after
    data, cost, cached = Y.call("search", params)
    items = data.get("items", [])
    ids = [i["id"]["videoId"] for i in items if i.get("id", {}).get("videoId")]
    # 통계 보강 (videos.list = 1 unit)
    stats = {}
    if ids:
        vdata, c2, _ = Y.call("videos", {"part": "statistics,contentDetails", "id": ",".join(ids)})
        cost += c2
        for v in vdata.get("items", []):
            stats[v["id"]] = v

    today = datetime.date.today().isoformat()
    slug = a.keyword.replace(" ", "_").replace("/", "_")
    jpath = Y.out_path("20_research", "keywords", f"api_{slug}_{today}.json")
    json.dump(data, io.open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    lines = [f"# API 검색 — {a.keyword} ({today})", "",
             f"> `search_videos.py` · order={a.order} · region={a.region}" + (f" · 최근 {a.days}일" if a.days else "") +
             f" · 쿼터 비용 {cost}{' (캐시)' if cached else ''}", "",
             "| # | 영상 | 채널 | 게시일 | 조회수 | 좋아요 | 길이 | 링크 |", "|---|---|---|---|---|---|---|---|"]
    for n, it in enumerate(items, 1):
        vid = it["id"].get("videoId", "")
        sn = it["snippet"]
        st = stats.get(vid, {})
        s = st.get("statistics", {})
        dur = Y.iso_dur_to_min(st.get("contentDetails", {}).get("duration"))
        lines.append(f"| {n} | {sn['title'][:45]} | {sn['channelTitle']} | {sn['publishedAt'][:10]} | "
                     f"{int(s.get('viewCount', 0)):,} | {int(s.get('likeCount', 0)):,} | {dur} | https://youtu.be/{vid} |")
    lines += ["", "## 발견 (수동 기입 — T1 주제카드 원료)", "- ", "", "## 파생 주제 후보", "- "]
    mpath = Y.out_path("20_research", "keywords", f"api_{slug}_{today}.md")
    io.open(mpath, "w", encoding="utf-8").write("\n".join(lines))
    print(f"OK: {len(items)}건 → {mpath} (쿼터 {cost})")


if __name__ == "__main__":
    main()
