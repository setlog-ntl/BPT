# -*- coding: utf-8 -*-
"""S2 댓글 원료 — 인기순 댓글 수집 (크롬 추출의 대체/보완 경로, 댓글_수집.md v2 ②)
사용: python fetch_comments.py <videoId|URL> [--max 200]
출력: 20_research/comments/raw_<videoId>.json + 미리보기 md (TOP 10)
비용: commentThreads.list = 1 unit/페이지(100개) — 저렴
룰: 인용·좋아요 수는 실데이터만 (창작 금지 — 댓글분석 SSOT 검증 7체크)
"""
import sys, io, json, argparse, datetime, re
import yt_common as Y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--max", type=int, default=200)
    a = ap.parse_args()
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", a.video)
    vid = m.group(1) if m else a.video.strip()

    comments, token, cost = [], None, 0
    while len(comments) < a.max:
        params = {"part": "snippet", "videoId": vid, "order": "relevance",
                  "maxResults": 100, "textFormat": "plainText"}
        if token:
            params["pageToken"] = token
        data, c, _ = Y.call("commentThreads", params)
        cost += c
        for it in data.get("items", []):
            s = it["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "text": s.get("textDisplay", ""),
                "likes": int(s.get("likeCount", 0)),
                "author": s.get("authorDisplayName", ""),
                "published": s.get("publishedAt", "")[:10],
                "replies": int(it["snippet"].get("totalReplyCount", 0)),
            })
        token = data.get("nextPageToken")
        if not token:
            break
    comments = comments[: a.max]

    jpath = Y.out_path("20_research", "comments", f"raw_{vid}.json")
    json.dump({"videoId": vid, "fetched": datetime.date.today().isoformat(),
               "count": len(comments), "comments": comments},
              io.open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    top = sorted(comments, key=lambda c: -c["likes"])[:10]
    lines = [f"# 댓글 원본 미리보기 — {vid} ({datetime.date.today().isoformat()})",
             f"> 인기순 {len(comments)}개 수집 · 쿼터 {cost} · 원본 = `raw_{vid}.json`",
             "> 분석은 [`10_system/cowork_prompts/댓글_수집.md`](../../10_system/cowork_prompts/댓글_수집.md) 4단 구조 + 언어뱅크 적립으로.", "",
             "| # | 좋아요 | 댓글 (200자 트림) |", "|---|---|---|"]
    for n, c in enumerate(top, 1):
        t = c["text"].replace("\n", " ").replace("|", "¦")[:200]
        lines.append(f"| {n} | {c['likes']:,} | {t} |")
    mpath = Y.out_path("20_research", "comments", f"raw_{vid}_미리보기.md")
    io.open(mpath, "w", encoding="utf-8").write("\n".join(lines))
    print(f"OK: 댓글 {len(comments)}개 → {jpath} (쿼터 {cost})")


if __name__ == "__main__":
    main()
