# 자동편집 테스트 결과 — 독서습관실패 이유3가지.mp4

> capcut-autoeditor v0.1 · Phase 1(무음 컷) 실제 영상 검증 · 2026-06-04

## 1. 입력 영상

| 항목 | 값 |
|---|---|
| 파일 | 촬영자료/독서습관실패 이유3가지.mp4 (124 MB) |
| 길이 | **13:38.58** (818.6초) |
| 해상도/코덱 | 2560×1440, 30fps, HEVC(H.265) |
| 오디오 | AAC, 스테레오, 44.1kHz |

## 2. 실행한 단계 (사이트 내부에서 실제 실행됨)

`ingest → silence → cutplan` — **7.4초** 소요.

1. **ingest**: 16kHz mono 오디오 추출(audio.wav, 26MB).
2. **silence**: ffmpeg silencedetect(노이즈 −30dB, 최소 0.6초)로 무음 감지.
3. **cutplan**: 무음 컷 결정을 합쳐 EDL(유지구간) 생성.

## 3. 결과 수치

| 지표 | 값 |
|---|---|
| 감지된 무음 구간 | **221개** |
| 컷된 무음 총량 | **2:00.27** (120.3초) |
| 유지 구간(EDL) | **222개** |
| 최종 길이(예상) | **11:38.30** (698.3초) |
| **절감률** | **14.7%** (원본 대비) |

> 컷 경계마다 0.15초 호흡(padding)을 남겨 자연스럽게 처리했습니다. 임계값은 `config.yaml`의 `silence.noise_db / min_silence_s / keep_padding_s`로 조정 가능합니다.

## 4. 산출물 (이 폴더 `_autoedit_work/`)

- `preview_trimmed.mp4` — **무음 제거 미리보기**(출력 46.1초, 원본 54.4초 구간 → 720p). 실제 컷 결과를 눈으로 확인용.
- `cutlist.csv` — 전체 컷/유지 구간 목록(443행, 타임코드·사유). 수동 검수/타 편집기 반영용.
- `project.json` — 파이프라인 상태(미디어·무음·EDL). 이후 단계가 이어서 사용.
- `audio.wav` — 추출 오디오.

## 5. 사이트 내부에서 못 한 것 + 이유

| 단계 | 상태 | 이유 |
|---|---|---|
| transcribe(전사) | ⛔ 미실행 | 작업 환경 네트워크 정책상 Whisper 모델 다운로드(HuggingFace)가 차단(403). 또한 13분 CPU 전사는 호출당 시간제한 초과. |
| ng_detect(NG/중복) | ⛔ 미실행 | 전사 결과 + 임베딩 모델 필요(동일 다운로드 제약). |
| subtitle / segment / recommend | ⛔ 대기 | 전사 결과 또는 LLM 키 필요. |

→ 이 단계들은 **사용자 PC(GPU 권장)** 에서 실행하는 것이 정확도·속도 모두 유리합니다(한국어는 `large-v3` 권장).

## 6. 내 PC에서 전체 파이프라인 돌리기

```bash
# 1) 프로젝트 준비 (capcut-autoeditor.zip 압축 해제 후)
cd capcut-autoeditor
pip install -e .
pip install faster-whisper sentence-transformers numpy   # 전사 + NG/중복
pip install pycapcut                                      # CapCut 드래프트 조립
pip install openai                                        # 자막 보정/구간/추천(선택)

# 2) 설정
cp config.example.yaml config.yaml
#   - asr.model: large-v3   (한국어 정확도)
#   - app.drafts_dir: CapCut 드래프트 폴더
export OPENAI_API_KEY=...   # 자막 LLM 보정 시

# 3) 실행 (이 영상 기준)
autoedit new "촬영자료/독서습관실패 이유3가지.mp4" --work ./_autoedit_work_local
autoedit run                       # 전체: 전사→무음→NG→컷→자막→조립→구간→추천
# 또는 단계별:
autoedit run transcribe ng_detect  # 전사 + NG/중복 테이크 감지만
autoedit run subtitle              # 자막 생성 + 맥락 보정
autoedit status
```

> 참고: 이 폴더의 `project.json`은 작업 환경 경로(audio.wav)를 담고 있어 그대로 재사용하기보다, 내 PC에서 `autoedit new`로 새로 시작하는 것을 권장합니다.

## 7. 다음 제안

- **NG/중복 테이크 감지(Phase 2)**: 대본(대본_독서습관실패99_v1.md)이 있으니, 전사 결과를 대본과 정렬해 "두 번 말한 구간"을 더 정확히 잡는 방식으로 고도화 가능.
- **구간화(Phase 5)**: 이 영상은 "3가지 이유" 구조 → 자동 주제 분할로 챕터 3개 + 도입/마무리를 잡기 좋은 케이스.
- **에셋 추천(Phase 6)**: 참조이미지/촬영자료의 카카오톡 클립들을 구간별 B-roll 후보로 매핑.
