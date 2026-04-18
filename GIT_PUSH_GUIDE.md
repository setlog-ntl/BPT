# GitHub Push 가이드

이 파일은 `C:\Dev\bizpt` 폴더를 `https://github.com/habitree/BPT` 에 **처음 올릴 때**의 1회용 가이드입니다. 완료 후 삭제하거나 아카이브해도 됩니다.

## 현재 상태 (2026-04-18 업데이트)

- ✅ 로컬 `C:\Dev\bizpt`: `git init`, 설정, **초기 커밋 완료**
  - `user.name = 최동혁` / `user.email = cdhrich@gmail.com`
  - `origin` = `https://github.com/habitree/BPT.git`
  - 커밋 메시지: `feat: 비즈니스PT 1주차 학습 정리 초기 커밋`
- ⚠️ 원격 `habitree/BPT`: Claude가 `main` 브랜치 부트스트랩용으로 만든 **README placeholder 커밋 1개** 존재
  - 로컬 커밋과 history가 분리(unrelated histories)되어 있어 일반 `push` 는 거부됨

## 한 줄 해결 (권장)

```bash
cd C:\Dev\bizpt
git push -u origin main --force
```

`--force`는 원격의 placeholder를 로컬 커밋으로 **덮어씁니다**. placeholder는 임시 파일이므로 잃을 게 없습니다.

인증 창이 뜨면 GitHub 계정(habitree)으로 로그인 (Git Credential Manager).

## 준비물 확인

PowerShell 또는 Git Bash에서:

```bash
git --version
```

Git이 설치되어 있지 않으면 <https://git-scm.com/download/win> 에서 설치.

---

## 1단계 · GitHub 빈 레포 (✅ 이미 완료)

- URL: <https://github.com/habitree/BPT>
- Clone URL: `https://github.com/habitree/BPT.git`

빈 레포 상태에서 첫 커밋을 받도록 구성되어야 합니다 (README·gitignore·license 체크 안 된 상태).
이미 체크되어 있다면 충돌이 날 수 있으니 로컬 푸시 전 `git pull origin main --rebase`를 먼저 실행하세요.

---

## 2단계 · 로컬에서 Git 초기화 + 초기 커밋

**Windows PowerShell 또는 Git Bash**를 `C:\Dev\bizpt`에서 연 뒤:

```bash
cd C:\Dev\bizpt

# 저장소 초기화 (main 브랜치로)
git init -b main

# (선택) 이 레포에만 적용할 커밋 정보 설정 — 전역 설정이 이미 있으면 건너뛰어도 됩니다
git config user.name "최동혁"
git config user.email "cdhrich@gmail.com"

# 모든 파일 스테이징
git add .

# 초기 커밋
git commit -m "Initial commit: 비즈니스PT 학습 정리 (1주차 종합)"
```

---

## 3단계 · GitHub에 푸시

```bash
# 원격 저장소 연결
git remote add origin https://github.com/habitree/BPT.git

# 푸시
git push -u origin main
```

처음 푸시 시 GitHub 로그인 창이 뜨면 계정 인증을 진행하세요
(Git Credential Manager가 알아서 팝업을 띄웁니다).

---

## 이후 변경사항 업데이트

```bash
cd C:\Dev\bizpt
git add .
git commit -m "변경 내용 요약"
git push
```

---

## 문제 해결

| 증상 | 원인/해결 |
|---|---|
| `fatal: not a git repository` | `git init` 을 아직 안 돌렸거나 다른 폴더에 있음. `cd C:\Dev\bizpt` 확인 후 재시도 |
| `remote origin already exists` | `git remote remove origin` 후 다시 `git remote add origin …` |
| `Authentication failed` | GitHub 비밀번호는 더 이상 안 됩니다. **Personal Access Token** 생성: <https://github.com/settings/tokens> → 토큰을 비밀번호 대신 입력. 또는 GitHub CLI (`gh auth login`) 사용 |
| 한글 파일명이 깨짐 | `git config --global core.quotepath false` |
| 커밋 메시지 한글이 물음표로 보임 | `git config --global i18n.commitEncoding utf-8` |

---

## 레포 이름 추천

- `bizpt` (짧고 직관적)
- `bizpt-notes` (학습 정리임을 명시)
- `business-pt-study` (영문 설명형)

Public 레포지만 강의 원본이 아닌 **개인 해석·재구성**만 담고 있으므로 저작권 이슈는 없습니다 (README에 이미 명시).
