# -*- coding: utf-8 -*-
"""S1 '기회' 축 판정 — 영상 통계 + 구독자 대비 성과(떡상 신호)
사용: python video_stats.py <videoId> [<videoId> ...]   (URL도 허용)
출력: 20_research/keywords/stats_<날짜>.md (append) — 조회수/구독자 비 ≥ 1.0 = 알고리즘 열림 신호
비용: videos.list + channels.list = 각 1 unit
"""
import sys, io, re, datetime
import yt_common as Y


def vid_of(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else s.strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    ids = [vid_of(x) for x in sys.argv[1:]]
    data, cost, _ = Y.call("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(ids)})
    items = data.get("items", [])
    ch_ids = sorted({v["snippet"]["channelId"] for v in items})
    subs = {}
    if ch_ids:
        cdata, c2, _ = Y.call("channels", {"part": "statistics", "id": ",".join(ch_ids)})
        cost += c2
        for c in cdata.get("items", []):
            subs[c["id"]] = int(c.get("statistics", {}).get("subscriberCount", 0) or 0)

    today = datetime.date.today().isoformat()
    lines = [f"\n## 통계 조회 {today} (쿼터 {cost})", "",
             "| 영상 | 채널 | 구독자 | 조회수 | **조회/구독 비** | 좋아요 | 길이 | 게시일 | 태그 수 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for v in items:
        sn, st = v["snippet"], v.get("statistics", {})
        sub = subs.get(sn["channelId"], 0)
        views = int(st.get("viewCount", 0))
        ratio = f"**{views / sub:.1f}**" if sub else "n/a"
        lines.append(f"| {sn['title'][:40]} | {sn['channelTitle']} | {sub:,} | {views:,} | {ratio} | "
                     f"{int(st.get('likeCount', 0)):,} | {Y.iso_dur_to_min(v['contentDetails']['duration'])} | "
                     f"{sn['publishedAt'][:10]} | {len(sn.get('tags', []))} |")
    lines.append("\n> 조회/구독 비 ≥ 1.0 = 구독자 대비 떡상 (T2 스코어카드 '기회' 축 근거)")
    mpath = Y.out_path("20_research", "keywords", f"stats_{today}.md")
    with io.open(mpath, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"OK: {len(items)}건 → {mpath} (쿼터 {cost})")


if __name__ == "__main__":
    main()
