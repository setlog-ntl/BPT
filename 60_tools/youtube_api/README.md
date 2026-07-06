# 60_tools/youtube_api — YouTube Data API v3 수집 도구

> S1(수요·기회 스코어)·S2(댓글 원료)·S9(공개 지표 추적)의 데이터 경로. 표준 라이브러리만 사용 — 별도 설치 불요 (Python 3.9+).

## 설치·키 설정

1. [Google Cloud Console](https://console.cloud.google.com/) → 프로젝트 → **YouTube Data API v3** 활성화 → API 키 발급.
2. 저장소 루트 `.env`에 한 줄 추가 (**절대 커밋 금지** — `.gitignore`가 `.env` 차단 중):
   ```
   YOUTUBE_API_KEY=발급받은키
   ```

## 스크립트 3종

| 스크립트 | 용도 (스테이지) | 사용 예 | 출력 | 비용 |
|---|---|---|---|---|
| `search_videos.py` | 키워드 → 상위 영상 (S1 수요) | `python search_videos.py "바이브코딩" --order viewCount --days 365` | `20_research/keywords/api_<키워드>_<날짜>.md+json` | **100+1** |
| `video_stats.py` | 영상 통계 + **조회/구독 비**(S1 기회 — 떡상 신호) | `python video_stats.py <URL 또는 ID ...>` | `20_research/keywords/stats_<날짜>.md` (append) | 1+1 |
| `fetch_comments.py` | 인기순 댓글 (S2 — 크롬 추출 대체/보완) | `python fetch_comments.py <URL> --max 200` | `20_research/comments/raw_<ID>.json` + 미리보기 | 1/100개 |

## 쿼터 규칙 (일일 10,000 units)

- **search.list = 100 units/호출로 비싸다** → 검색은 **하루 상한 20회(2,000 units)** 를 넘기지 않는다. videos/channels/commentThreads = 1 unit로 저렴.
- **캐시**: 동일 요청은 24h 내 재호출 금지 — `_cache/`에 자동 캐시(비용 0). 실행 로그 = `_logs/run.log`.
- 대량 키워드 스캔은 뷰트랩(코워크)이 1차, API는 검증·보완이 원칙.

## 사용처 매핑

- **S1**: search→stats로 T2 스코어카드 '수요·기회' 근거 채움 (topic-scout)
- **S2**: fetch_comments → `10_system/cowork_prompts/댓글_수집.md` v2의 ② API 경로
- **S9**: video_stats로 자기 영상 공개 지표 추적 (analytics-reviewer — 스튜디오 지표는 사용자 제공)
