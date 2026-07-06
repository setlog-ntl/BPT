# AI는 평균을 주고, 책은 깊이를 준다 — 자동 영상 생성 파이프라인

업로드해주신 기획서(BODY 1을 메인 축으로 격상)를 바탕으로 만든
**10분짜리 유튜브 영상 자동 생성 파이프라인**입니다.

## 결과물 (output/)

| 파일 | 설명 |
|---|---|
| `AI_평균_책_깊이_10min_subs.mp4` | **자막 burn-in 최종본 — 바로 업로드 가능** (1280×720, 9분 20초, 21MB, BGM only) |
| `AI_평균_책_깊이_10min.mp4` | 자막 없는 버전 (사이드카 SRT용) |
| `subtitles.srt` | 한국어 자막 38구간, YouTube 자막 파일로 그대로 사용 가능 |

## 톤·구성 요약

- **메시지 축**: "AI는 평균을 주고, 책은 깊이를 준다"
- **톤**: 논리·인사이트형 (차분·설득)
- **타임라인 (38씬, 9:20)**
  - HOOK 0:00–0:42 — AI 시대에 머스크/게이츠가 더 읽는 역설
  - INTRO 0:42–1:10 — 오늘의 한 문장 + 5+3 미리보기
  - **BODY 1 1:10–3:30 — 평균 vs 깊이 (메인 축, 9씬)**
  - BODY 2 3:30–4:46 — 좋은 프롬프트는 사전지식에서
  - BODY 3 4:46–5:50 — 독해력 = 새로운 문해력
  - BODY 4 5:50–6:55 — 트렌드는 AI에서, 본질은 책에서
  - BODY 5 6:55–7:55 — 집중력은 자산이다
  - 실전 7:55–9:15 — AI 시대 독서법 3가지
  - CTA 9:15–9:20 — 댓글 챌린지 + 다음 영상 예고

## 어떻게 만들어졌나 (자동화 파이프라인)

```
scenes.py        ← 38씬 데이터 (대본·자막·강조색)
  │
  ├─ slides.py   ← Pillow로 1920×1080 키네틱 타이포 슬라이드 38장 PNG 생성
  ├─ tts_gen.py  ← Edge TTS(ko-KR-SunHi)로 씬별 한국어 내레이션 mp3 생성
  ├─ bgm_gen.py  ← numpy로 절차생성 lo-fi 앰비언트 BGM 10분 wav
  ├─ srt_gen.py  ← 씬별 노출 시간으로 SRT 자막 생성
  │
  └─ compose_ffmpeg.py  ← ffmpeg로 슬라이드+오디오 합성 → MP4 + 자막 burn-in
```

오케스트레이터 `run_all.py` 한 번 실행하면 위 단계가 순서대로 자동 실행됩니다.

## 로컬에서 실행하기 (윈도우 / 맥)

```bash
# 1. 의존성 설치
pip install edge-tts moviepy Pillow numpy
# ffmpeg 설치 (윈도우: https://www.gyan.dev/ffmpeg/builds/, choco install ffmpeg)

# 2. 한 번에 모두 실행 (TTS 내레이션 포함)
python run_all.py

# 옵션
python run_all.py --no-tts     # TTS 스킵 (인터넷 안 될 때)
python run_all.py --no-burn    # 자막 burn-in 스킵
```

샌드박스 환경(Edge TTS 차단)에서는 BGM 위주 영상으로 빌드되었지만,
**로컬에서 실행하면 한국어 내레이션이 자동으로 합성**되어 BGM과 더킹 믹싱됩니다.

## 톤·보이스 변경 방법

`tts_gen.py` 상단의 변수만 바꾸면 됩니다.

```python
VOICE = "ko-KR-SunHiNeural"   # 차분한 여성 (현재 기본)
# 대안:
# VOICE = "ko-KR-InJoonNeural"   # 신뢰감 있는 남성
# VOICE = "ko-KR-BongJinNeural"  # 묵직한 남성
# VOICE = "ko-KR-JiMinNeural"    # 밝은 여성
RATE  = "+5%"  # 속도 (-50% ~ +200%)
PITCH = "+0Hz"
```

## 대본 수정·재빌드

- 한 씬 텍스트만 바꾸려면 `scenes.py`에서 해당 씬의 `narration` / `big1` / `big2` 수정
- 슬라이드 색상·폰트는 `slides.py`의 `COLORS`·`PART_COLORS` 변수로 통제
- 변경 후: `python run_all.py` (캐시 덕에 변경된 씬만 다시 빌드)

## 다른 주제로 영상 만들기

`scenes.py`의 SCENES 리스트만 통째로 갈아끼우면 동일한 비주얼 시스템으로
다른 주제 영상도 자동 생성됩니다. 비즈PT 콜드 후킹 시리즈 다음 편
"독서 환경 세팅" 같은 영상도 같은 파이프라인으로 30분 안에 빌드 가능합니다.
