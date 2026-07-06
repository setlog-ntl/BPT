---
주제: readingtree 연계 — 정리 문서 위치 안내
역할: bizpt 프로젝트에서 readingtree 관련 정보를 참조할 때의 단일 진입점
원본 정리: readingtree 자체 프로젝트에서 관리 (Claude Code로 사용자가 직접 작성)
---

# readingtree 연계

> bizpt(이 프로젝트)는 readingtree를 **유튜브 채널의 도착지점/랜딩 자산** 중 하나로 활용한다.
> readingtree 서비스 자체의 정의·기능·로드맵 등 **원본 정리는 readingtree 프로젝트에서 관리**한다.
> 이 문서는 **그 원본 정리 위치를 가리키는 인덱스/포인터**이며, 콘텐츠 기획·랜딩 설계 시 항상 여기를 거쳐 참조한다.

---

## 📌 readingtree 프로젝트 정리 문서 경로

> 마지막 갱신: **2026-05-03** (readingtree 저장소 직접 검증)
> 서비스 정체성: **Habitree Reading Hub (ReadTree v4.0.0)** · Next.js + Supabase + Gemini AI · 독서 기록·공유 플랫폼

| 항목 | 1순위 경로 | 보조 경로 (선택) |
|---|---|---|
| **readingtree 프로젝트 루트** | `C:\Dev\readingtree\` | — |
| **서비스 개요 / 정체성** | `C:\Dev\readingtree\README.md` (한 줄 정의·핵심 가치 4개·Why-now AI 시대) | `doc\idea\00_통합_고도화_기획안.md` |
| **기능·기술 정리** | `C:\Dev\readingtree\doc\architecture\ARCHITECTURE_OVERVIEW.md` | `doc\architecture\FEATURE_MAP.md` · `MODULE_MAP.md` · `DEPENDENCY_RULES.md` |
| **타깃 사용자 / 페르소나** | `C:\Dev\readingtree\doc\plan\페르소나-기반-확장기능-기획문서.md` | `doc\audit\pre-launch-audit-2026-02-19.md` |
| **사용 시나리오** | `C:\Dev\readingtree\doc\planning\reading-forest-plan.md` (독서 숲 핵심 흐름) | `doc\features\GROUP_BOOK_NOTES.md` · `GROUPS_ENHANCEMENT.md` |
| **로드맵 / 다음 릴리즈** | `C:\Dev\readingtree\doc\launch-checklist.md` | `doc\planning\enhancement-plan-2026.html` · `doc\plans\HOME_SCREEN_UPDATE_PLAN.md` · `doc\idea\DECISION_SUMMARY.md` |
| **브랜드 자산 (로고·색상·톤)** | `C:\Dev\readingtree\doc\design\DESIGN_GUIDELINES.md` | `doc\design\COMPONENT_CATALOG.md` · `doc\design\Theme\` · `public\img\` · `public\readtree-trees-icon-{24,48,96}.png` |
| **수익화 모델** ✨신규 | `C:\Dev\readingtree\doc\business\MONETIZATION_STRATEGY.md` | `doc\business\SUBSCRIPTION_3TIER.md` · `AI_PRICING_PLAN.md` · `BOOK_AFFILIATE_STRATEGY.md` · `COST_AND_POINT_MASTER.md` |
| **메뉴·정보 구조** ✨신규 | `C:\Dev\readingtree\doc\menu-structure.md` | — |
| **법무·약관** ✨신규 | `C:\Dev\readingtree\doc\legal\` (폴더) | — |

**확인:** 모든 1순위 경로는 2026-05-03에 readingtree 저장소에서 실제 존재 검증 완료. 이후 readingtree에서 큰 폴더 재정렬이 있으면 [`10_system/prompts/readingtree_인덱스_갱신.md`](../../10_system/prompts/readingtree_인덱스_갱신.md) 프롬프트로 재갱신.

---

## bizpt에서 readingtree를 참조하는 시점

| 작업 | 참조 항목 |
|---|---|
| 풀링 콘텐츠 기획 (4주차~) | 서비스 개요, 타깃 페르소나 — 콘텐츠 톤·후크 정렬 |
| 키 콘텐츠 기획·제작 (3주차/12~18주차) | 기능, 사용 시나리오 — 상품/서비스 후킹 포인트 |
| 랜딩 페이지 설계 (19~23주차) | 사용 시나리오, 브랜드 자산 — 전환 동선 설계 |
| 플랫폼 확장 (24~29주차) | 로드맵 — bizpt 채널·플랫폼 확장과 readingtree 릴리즈 일정 정렬 |

---

## 갱신 규칙
- readingtree 프로젝트의 원본 문서가 갱신되면 → 이 인덱스 표만 확인 (내용은 readingtree 쪽에 있음)
- bizpt에서 readingtree 관련 새로운 정리가 필요해지면 → readingtree 프로젝트에 작성 후 여기에 경로만 추가
- **bizpt 안에 readingtree 본문을 복제하지 않는다** (단일 진실 원천 유지)
- 정기 갱신 (분기 1회 권장): [`10_system/prompts/readingtree_인덱스_갱신.md`](../../10_system/prompts/readingtree_인덱스_갱신.md) 프롬프트 실행

---

## 갱신 이력
| 일자 | 변경 | 출처 |
|---|---|---|
| 2026-05-03 | 표준 매핑 적용 — 1순위 경로 7개 + 보조 경로 + 신규 행 3개(수익화·메뉴·법무) 채움. 모든 1순위 경로 readingtree 저장소에서 실제 존재 검증. | Claude 자동 갱신 (readingtree v4.0.0 구조 기준) |
| (이전) | 인덱스 표 초기 생성 — 모든 항목 `<TBD>` | 사용자 수동 |
