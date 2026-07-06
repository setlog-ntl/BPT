# AI 음악 프롬프트 모음 — 채널 "AI보다 읽는 사람"

> ⚠️ **2026-06-13 채널명 전환**: 채널명이 **"AI보다 읽는 사람"**으로 바뀌었다. 아래 가사(LYRICS)의 후렴 시그니처 **"그럼에도 불구하고"는 채널 사인오프 "AI는 답을, 읽는 사람은 질문을."로 바꿔** 생성한다. 곡 제목·후렴도 새 시그니처 기준. (아래 가사는 구 채널명 시기 초안 — 새 시그니처로 변주해 재생성)
>
> 복사해서 바로 붙여넣는 실전 프롬프트. 기획 맥락은 → [`BGM_기획문서.md`](BGM_기획문서.md) · 도구 선택은 → [`무료_음악생성_도구_비교.md`](무료_음악생성_도구_비교.md)
>
> **무료 제작 권장 도구 = Sonauto** (무제한·무료·한국어·instrumental/vocal). 아래 프롬프트는 Sonauto·Suno·Udio·MiniMax에 **모두 호환**(STYLE = 영어 스타일 설명, LYRICS = 가사 구조). 단 무료 상업 사용은 도구별로 다름 → 비교 문서 §1·§4 확인.
>
> **도구별 입력 방법**
> | 도구 | 스타일 칸 | 가사(vocal) | instrumental(가사 없음) |
> |---|---|---|---|
> | **Sonauto**(권장·무료) | `STYLE` 블록 붙여넣기 | `LYRICS` 블록 붙여넣기 | **"No Lyrics" 버튼** 클릭 |
> | Suno | Style of Music 칸 | Lyrics 칸 | `[Instrumental]`만 + **Instrumental 토글 ON** |
> | Udio | 스타일 입력 | 가사 입력 | Instrumental 옵션 |
> | MiniMax 2.6 | 스타일 프롬프트 | 가사 입력(또는 Lyrics Optimizer 자동) | 무보컬 토글 |
>
> **공통 팁**
> - **곡명:** `Title` 값 그대로 사용.
> - 한 곡당 2~4회 생성 → 채널 톤에 맞는 것 채택. 채택 결과·사용 도구·곡 ID는 기획문서 §8 로그에 기록.
> - `[Verse] [Chorus]` 등 구조 태그는 Suno/Sonauto에서 잘 먹고, 도구에 따라 무시될 수 있음(가사 자체는 그대로 사용됨).
>
> 작성: 2026-06-07 · 갱신: 2026-06-07 (무료 도구 호환 추가)

---

## 공통 NEGATIVE / 회피 지시 (모든 STYLE 끝에 이미 포함됨, 참고용)

```
avoid: aggressive EDM drop, trap hi-hats, dubstep, harsh synth lead,
clickbait build-up, distorted bass, autotune-heavy vocals, loud mastering
```
채널 톤 = 빠른 시대의 **느린 자리**. 과자극·드롭·트랩 금지.

---

# 컨셉 A — "느린 자리" (메인/풀링 테마) 🟢

> 풀링 영상 배경·표준 인트로·채널 기본 BGM. 말소리를 덮지 않는 잔잔함.

## A-1. Instrumental (가사 없음)

**Title:** `느린자리_A_instrumental`

**STYLE**
```
warm lo-fi acoustic, felt piano, soft fingerpicked acoustic guitar,
gentle analog pads, subtle page-turning paper foley, cozy room tone,
contemplative and intimate, slow and breathing, 84 bpm,
background music for voiceover, low-key, no vocals, leaves space,
analog tape warmth, organic hand-played feel.
avoid: aggressive EDM drop, trap hi-hats, harsh synth lead,
clickbait build-up, distorted bass, loud mastering.
```

**LYRICS:** 가사 없음 — **Sonauto: "No Lyrics" 버튼** / Suno·기타: 가사 칸에 `[Instrumental]`만 + Instrumental 토글 ON

---

## A-2. Vocal (가사 있음)

**Title:** `느린자리_A_vocal`

**STYLE**
```
warm acoustic singer-songwriter, soft intimate Korean female vocal
(or breathy male vocal), felt piano, fingerpicked guitar, gentle pads,
contemplative folk, 84 bpm, close-mic whisper-sing, sincere, unhurried,
subtle paper-turning foley, analog warmth.
avoid: aggressive drop, trap hi-hats, autotune-heavy vocals, loud mastering.
```

**LYRICS**
```
[Intro]
(가벼운 숨, 피아노)

[Verse]
세상은 빠르게 답을 건네고
나는 한 페이지에 머물러요
모두가 스쳐 지나간 자리에
조용히 앉아 있어요

[Chorus]
그럼에도 불구하고
나는 오늘도 펼쳐요
빠른 시대의 느린 자리에서
한 줄, 그럼에도

[Outro]
오늘도, 그럼에도 불구하고
(페이드 아웃)
```

---

# 컨셉 B — "그럼에도 불구하고" (키/감성·전환 테마) 🟡

> 키 영상 후반·랜딩·시즌 회고. 역접 후 따뜻하게 차오르는 감동.

## B-1. Instrumental (가사 없음)

**Title:** `그럼에도_B_instrumental`

**STYLE**
```
cinematic acoustic, emotional indie folk, felt piano lead,
warm cello and violin swells, fingerpicked acoustic guitar,
soft restrained kick, building from quiet to warm climax,
sincere and uplifting without being grand, 92 bpm, post-rock restraint,
a moment of pause then gentle rise, organic, heartfelt, no vocals.
avoid: aggressive EDM drop, trap hi-hats, bombastic orchestra hits,
clickbait build-up, loud mastering.
```

**LYRICS:** 가사 없음 — **Sonauto: "No Lyrics" 버튼** / Suno·기타: 가사 칸에 `[Instrumental]`만 + Instrumental 토글 ON

---

## B-2. Vocal (가사 있음)

**Title:** `그럼에도_B_vocal`

**STYLE**
```
cinematic acoustic ballad, sincere Korean vocal (warm mid-range),
felt piano, cello and violin swells, fingerpicked guitar,
emotional indie folk, building from intimate verse to warm chorus,
92 bpm, heartfelt, honest, not overproduced, organic dynamics.
avoid: aggressive drop, trap hi-hats, autotune-heavy vocals, power-ballad cheese.
```

**LYRICS**
```
[Intro]
(피아노, 첼로 한 음)

[Verse]
다들 그래요, 답은 이미 넘친다고
손끝 하나면 다 안다고
그런데 왜 나는 자꾸
더 깊은 곳이 궁금할까

[Pre-Chorus]
흐름은 인정해요
빨라도 괜찮아요
그래도 멈춰 서는 자리

[Chorus]
그럼에도 불구하고
나는 질문을 만들어요
AI는 답을 주고
책은 나에게 물어요
그럼에도, 그럼에도 불구하고

[Outro]
오늘도, 그럼에도 불구하고
읽어요, 우리
```

---

# 컨셉 C — "질문이 시작되는 순간" (쇼츠/유입 테마) 🔴

> 쇼츠·풀링 클립·커뮤니티. 3초 내 시선 고정, 경쾌하되 채널 톤 유지. loop-friendly.

## C-1. Instrumental (가사 없음)

**Title:** `질문의순간_C_instrumental`

**STYLE**
```
upbeat lo-fi chillhop, bouncy electric piano, warm marimba,
light finger snaps and soft claps, smooth round bass, subtle paper foley,
curious and playful but cozy, immediate catchy hook in first 2 seconds,
loop-friendly, 102 bpm, head-nodding groove, organic, no vocals.
avoid: aggressive EDM drop, trap hi-hats, harsh synth, over-stimulating fx,
distorted bass, loud mastering.
```

**LYRICS:** 가사 없음 — **Sonauto: "No Lyrics" 버튼** / Suno·기타: 가사 칸에 `[Instrumental]`만 + Instrumental 토글 ON

---

## C-2. Vocal (가사 있음)

**Title:** `질문의순간_C_vocal`

**STYLE**
```
upbeat lo-fi chillhop with light Korean vocal hook, bouncy electric piano,
warm marimba, finger snaps, smooth bass, playful and curious yet cozy,
short catchy vocal hook, 102 bpm, loop-friendly, casual and warm,
conversational singing, not shouty.
avoid: aggressive drop, trap hi-hats, autotune-heavy vocals, loud mastering.
```

**LYRICS**
```
[Intro / Hook]
그럼에도 불구하고 — 오늘도 한 줄

[Verse]
빠르게 스크롤, 빠르게 답
근데 남는 건 별로 없잖아
잠깐 멈춰, 한 페이지
거기서 질문이 시작돼

[Chorus / Hook]
그럼에도 불구하고
읽는 사람이 멀리 가
한 줄, 한 줄, 그럼에도
오늘도 펼쳐 봐

[Outro]
(책장에서 본편으로 — )
```

---

# BONUS — 사운드 로고 (3초 오디오 인트로) 🔔

> 채널 정체성 문서 §08-03 사양: 종이 넘기는 소리 1초 + 부드러운 단음 1초 + 사인오프와 동일한 키.
> 모든 영상 0:00에 동일 재생. 컨셉 A 인트로에서 잘라 쓰거나 아래로 단독 생성.

**Title:** `사운드로고_3초`

**STYLE**
```
3-second audio logo / sonic branding, single page-turning paper sound,
then one warm soft felt-piano note with gentle reverb tail,
intimate, calm, signature sting, no drums, no vocals, ends on an open note.
avoid: loud, aggressive, synth, fanfare.
```

**LYRICS:** 가사 없음 — **Sonauto: "No Lyrics" 버튼** / Suno·기타: 가사 칸에 `[Instrumental]`만 + Instrumental 토글 ON

> 생성 후 0~3초 구간만 트리밍. "open note(질문하듯 끝나는 음)"는 골드 시그니처 모티브와 연결 — 같은 음정을 컨셉 A 인트로에 재사용하면 사운드 통일성 확보.

---

## 빠른 체크리스트 (생성 직전)

- ☐ **무료 제작이면 Sonauto** 사용(무제한·한국어·instrumental/vocal) — 도구 선택은 `무료_음악생성_도구_비교.md`
- ☐ Style 칸 = 영어 블록 그대로 / Lyrics 칸 = 한국어(또는 instrumental은 No Lyrics)
- ☐ instrumental은 Sonauto **"No Lyrics" 버튼**(Suno는 Instrumental 토글) 확인
- ☐ vocal 후렴에 "그럼에도 불구하고" 들어갔는지
- ☐ 과자극·드롭·트랩 없는지 (생성물 청취 시 재확인)
- ☐ 채택본 → `BGM_기획문서.md §8 제작 로그`에 **사용 도구·곡 ID·생성일** 기록
- ☐ **발행(수익화) 전 상업 사용 권한 확인** — Suno/Udio 무료는 비상업(수익화 불가), Sonauto는 §4 서면 확인, MiniMax 베타는 상업 OK
