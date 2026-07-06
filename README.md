# bizpt — 「바이브코딩 치트키」 🔑 유튜브 제작 OS

> 채널의 영상 1편 전 과정(기획→검증→패키징→대본→소스→제작→편집→업로드→성과분석)을 **S0~S9 파이프라인**으로 지휘하는 저장소.
> **Repo**: <https://github.com/habitree/BPT> · v2 전면개편: 2026-07-06 (`overhaul/youtube-os` — 상세 이력 `90_archive/2026-07_전면개편/`)

## 시작하기

| 무엇을 하려면 | 어디로 |
|---|---|
| **세션 시작 (Claude Code)** | [`CLAUDE.md`](CLAUDE.md) — 자동 로딩 진입점 (하드 룰·파이프라인 지도·에이전트 맵) |
| 영상 1편 만들기 | [`10_system/운영매뉴얼.md`](10_system/운영매뉴얼.md) — "영상 1편의 일생" 1페이지 |
| 채널 변수 확인 (채널명·아이템·보이스) | [`00_channel/channel_config.md`](00_channel/channel_config.md) — 변수 SSOT |
| 지시 → 담당 찾기 | [`10_system/registry.md`](10_system/registry.md) — 스테이지 라우팅 |
| 전략("왜") | [`프로젝트_방향성.md`](프로젝트_방향성.md) |
| SPA 열람 | [`index.html`](index.html) — hash 라우팅 단일 페이지 (GitHub Pages) |

## 저장소 구조 (숫자 = 파이프라인 흐름)

```
00_channel/    채널 전략 — channel_config(변수 SSOT)·identity·okr·series
10_system/     파이프라인 OS — registry·stages(S0~S9)·guides·templates(T1~14)·checklists(G1~5)·prompts·cowork_prompts
20_research/   시장·시청자 데이터 — topics(주제뱅크)·keywords(뷰트랩·API)·comments(댓글분석)·competitors·audience(언어뱅크)
30_videos/     ★ 영상 단위 폴더 (1 video = 1 project) — _index.md 현황 보드 + NNN_슬러그/
40_assets/     공용 제작 자산 — bgm·fonts·brand·prompts(생성 뱅크)·자산_라이브러리(ID 카탈로그)
50_knowledge/  교육 축 — 비즈니스PT 강의 정리(lectures)·reference (파이프라인 룰의 지식 공급원)
60_tools/      도구 — check_links.py(링크체커)·youtube_api(수집 3종)·shorts_pipeline
90_archive/    동결 보관 — _redirect_map.md(구→신 경로 전수)
raw/           강의 필사 원본 (불변)
docs/          SPA 전시실 — item/(SPA 직접 참조 3파일 잔류)
대본/           SPA 잔류 룰북 2종(_기획기준) + 대용량 미디어 원본(키컨텐츠)
content/·assets/  SPA 지원 파일
```

## 핵심 규칙 3줄

1. **패키징 퍼스트** — 제목·썸네일(G2 사용자 승인) 전에 대본을 쓰지 않는다.
2. **변수는 channel_config 참조만** — 아이템·시리즈·보이스를 시스템 문서에 하드코딩하지 않는다.
3. **삭제 금지·md 원천** — 제거는 `90_archive/` 이동, HTML은 md의 뷰. 이동 시 링크체커(`python 60_tools/check_links.py`) 신규 사망 0건.

## 변경 이력
| 날짜 | 변경 |
|---|---|
| 2026-07-06 | **v2 전면 재작성** — 유튜브 제작 OS 구조 반영 (전면개편 PHASE 7). v1(학습 아카이브 안내) 이력은 git 히스토리 |
