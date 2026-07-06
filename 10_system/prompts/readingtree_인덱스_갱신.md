# readingtree 인덱스 갱신

## 목적
readingtree 프로젝트(별도 저장소)에서 정리·갱신된 문서 위치를 bizpt의 [`50_knowledge/reference/readingtree_연계.md`](../../50_knowledge/reference/readingtree_연계.md) **인덱스 표에 반영**한다. bizpt 안에 readingtree 본문을 절대 복제하지 않는다.

---

## 입력 (사용자가 제공)
- **readingtree 프로젝트 루트 경로** (정확한 값): 기본 `C:\Dev\readingtree\`
- **갱신할 항목별 실제 경로** — 표를 직접 채우지 않아도 됨. 아래 §"표준 매핑(2026-05-03 검증)"이 그대로 쓰일 수 있다면 그 경로 사용.

---

## 사전 참조
1. `CLAUDE.md` (루트) — 특히 §4.2 (readingtree 룰)
2. `50_knowledge/reference/readingtree_연계.md` — 갱신 대상 인덱스
3. `프로젝트_방향성.md` §3 기둥 ③

---

## 표준 매핑 (2026-05-03 readingtree 저장소 구조 기준)

readingtree = **Habitree Reading Hub (ReadTree v4.0.0)** · Next.js · 독서 기록·공유 플랫폼.
실제 검증된 경로 (사용자가 readingtree에서 큰 구조를 바꾸지 않은 한 그대로 사용 가능):

| 항목 | 1순위 경로 | 보조 경로 (선택) |
|---|---|---|
| **서비스 개요 / 정체성** | `C:\Dev\readingtree\README.md` (프로젝트 한 줄 정의 + 핵심 가치 4개 + Why-now AI 시대) | `doc\idea\00_통합_고도화_기획안.md` (통합 고도화 비전) |
| **기능·기술 정리** | `C:\Dev\readingtree\doc\architecture\ARCHITECTURE_OVERVIEW.md` | `doc\architecture\FEATURE_MAP.md` · `doc\architecture\MODULE_MAP.md` · `doc\architecture\DEPENDENCY_RULES.md` |
| **타깃 사용자 / 페르소나** | `C:\Dev\readingtree\doc\plan\페르소나-기반-확장기능-기획문서.md` | `doc\audit\pre-launch-audit-2026-02-19.md` (사전 점검에 사용자 가설 포함) |
| **사용 시나리오** | `C:\Dev\readingtree\doc\planning\reading-forest-plan.md` (독서 숲 핵심 흐름) | `doc\features\GROUP_BOOK_NOTES.md` · `doc\features\GROUPS_ENHANCEMENT.md` |
| **로드맵 / 다음 릴리즈** | `C:\Dev\readingtree\doc\launch-checklist.md` (런치 체크리스트) | `doc\planning\enhancement-plan-2026.html` · `doc\plans\HOME_SCREEN_UPDATE_PLAN.md` · `doc\idea\DECISION_SUMMARY.md` |
| **브랜드 자산 (로고·색상·톤)** | `C:\Dev\readingtree\doc\design\DESIGN_GUIDELINES.md` | `doc\design\COMPONENT_CATALOG.md` · `doc\design\Theme\` · `public\img\` (실제 이미지 자산) · `public\favicon.ico` · `public\readtree-trees-icon-*.png` |
| **수익화 모델** (선택) | `C:\Dev\readingtree\doc\business\MONETIZATION_STRATEGY.md` | `doc\business\SUBSCRIPTION_3TIER.md` · `doc\business\AI_PRICING_PLAN.md` · `doc\business\BOOK_AFFILIATE_STRATEGY.md` |
| **메뉴·정보 구조** (선택) | `C:\Dev\readingtree\doc\menu-structure.md` | — |
| **법무·약관** (선택) | `C:\Dev\readingtree\doc\legal\` (폴더 인덱스) | — |

---

## 작업 절차
1. **사용자에게서 경로 변수를 받음** (또는 위 §"표준 매핑"이 그대로 적용 가능한지 확인 후 사용).
2. `50_knowledge/reference/readingtree_연계.md`를 읽어 현재 인덱스 표 확인.
3. **표 갱신**:
   - `<TBD>` 부분을 실제 경로로 교체 (위 매핑 표 참조)
   - 새 항목이 생겼으면(예: 수익화 모델) 표에 행 추가
   - 변경 일시를 갱신 (`마지막 갱신: YYYY-MM-DD`)
4. **점검** — 표에 적은 경로가 실제로 존재하는지 빠르게 확인:
   ```powershell
   Get-Item "C:\Dev\readingtree\<경로>"  # 또는 Bash: ls
   ```
   존재하지 않으면 사용자에게 readingtree 프로젝트 안에서 정확한 경로를 다시 받음.
5. **bizpt 본문 복제 점검** — bizpt 안 어딘가에 readingtree 본문이 복제된 흔적이 있으면 제거 후 인덱스 항목으로 대체.
6. **변경 이력 추가** — `readingtree_연계.md` 하단 "갱신 이력" 섹션에 한 줄 기록 (예: `2026-05-03 — 표준 매핑 적용, 7개 1순위 경로 채움 / Claude 자동`).

---

## 산출물 형식 / 저장 위치
- 변경 대상은 **단일 파일**: `50_knowledge/reference/readingtree_연계.md`
- 신규 파일 생성 없음 (단일 진실 원천 유지)

---

## 완료 체크리스트
- [ ] `<TBD>` 표시가 더 이상 남아있지 않은가 (또는 의도적으로 남긴 항목인가)
- [ ] 모든 경로가 절대 경로(또는 일관된 형식)로 표기됐는가
- [ ] 변경 일자가 표시됐는가
- [ ] bizpt 다른 문서들이 readingtree를 참조할 때 이 인덱스를 거치고 있는가 (직접 참조 금지)
- [ ] readingtree 본문이 bizpt 안에 복제되지 않았는가
- [ ] 표에 적은 1순위 경로가 실제로 readingtree에 존재하는가 (스폿 체크)

---

## readingtree 프로젝트 구조 빠른 참조 (2026-05-03)

루트:
- `README.md` (한 줄 정의 + 핵심 가치 + 주요 기능 + 기술 스택)
- `package.json` (Next.js + React + Supabase + Gemini AI 등)
- `app/`, `components/`, `lib/`, `hooks/`, `contexts/`, `types/` (Next.js 표준)

`doc/` 풀 카테고리:
- **architecture/** — ARCHITECTURE_OVERVIEW · FEATURE_MAP · MODULE_MAP · DEPENDENCY_RULES + `modules/`
- **business/** — MONETIZATION_STRATEGY · SUBSCRIPTION_3TIER · AI_PRICING_PLAN · BOOK_AFFILIATE_STRATEGY · COST_AND_POINT_MASTER · PROFITABILITY_REVIEW_2026Q2 + 대시보드 HTML
- **idea/** — 00_통합_고도화_기획안 · 01~06 전문가 분석 · DECISION_SUMMARY · LINEAR_ISSUES_TEMPLATE
- **plan/** — 페르소나-기반-확장기능-기획문서 · ai-restructure 시리즈 · points-gamification
- **planning/** — enhancement-plan-2026 · reading-forest-plan · record-redesign-prototype
- **plans/** — HOME_SCREEN_UPDATE_PLAN · POINTS_DASHBOARD_PLAN
- **features/** — GROUP_BOOK_NOTES · GROUPS_ENHANCEMENT
- **design/** — DESIGN_GUIDELINES · COMPONENT_CATALOG · `Theme/` · 모바일 최적화 · UX/UI 개선 등
- **audit/** — pre-launch-audit · SECURITY_AUDIT
- 기타: agents · ai · api · cleanup · components · connect · database · governance · launch-checklist.md · legal · log · menu-structure.md · migration · music · operations · payment · pmo · point-strategy · qa-inspection · question

`.agent/rules/` — 도메인별 에이전트 룰 (admin · ai · analytics · auth-session · data · deploy · engagement · groups · i18n · identity · legal · library 등)

`public/` 브랜드 자산:
- `favicon.ico` · `icon.png` · `readtree-trees-icon-{24,48,96}.png` · `manifest.json`
- `fonts/`, `animations/`, `images/`, `music/`, `payment-flow/`

---

## 갱신 후 권장 후속
- bizpt 측 콘텐츠 기획에서 readingtree를 후킹·랜딩으로 사용할 때 새로 채워진 1순위 경로를 직접 참고 (bizpt 안에 복제 금지).
- readingtree 쪽 README나 architecture가 크게 바뀌면 본 프롬프트의 §"표준 매핑"을 한 번 더 검증.
