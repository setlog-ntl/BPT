# -*- coding: utf-8 -*-
"""PHASE 4 이동 드라이버 — 배치 파일(src TAB dst)을 읽어 이동 실행.
- git 추적 파일이면 `git mv`, 아니면 os 이동 (폴더는 통째 이동 시 내부 추적 파일 개별 git mv 처리)
- 모든 이동을 90_archive/_redirect_map.md 에 누적 기록
사용: python _migration/tools/mig.py <batch.tsv> <배치라벨>
"""
import os, sys, subprocess, io, datetime

ROOT = r"C:\Dev\bizpt"
MAP = os.path.join(ROOT, "90_archive", "_redirect_map.md")

def tracked_under(path_rel):
    r = subprocess.run(["git", "ls-files", "--", path_rel], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    return [l for l in r.stdout.splitlines() if l.strip()]

def ensure_map():
    os.makedirs(os.path.dirname(MAP), exist_ok=True)
    if not os.path.exists(MAP):
        io.open(MAP, "w", encoding="utf-8").write(
            "# _redirect_map — 구 경로 → 신 경로 전수 기록 (전면개편 PHASE 4)\n\n"
            "| 배치 | 구 경로 | 신 경로 |\n|---|---|---|\n")

def log_move(batch, src, dst):
    io.open(MAP, "a", encoding="utf-8").write(f"| {batch} | `{src}` | `{dst}` |\n")

def move(src_rel, dst_rel, batch):
    src = os.path.join(ROOT, src_rel)
    dst = os.path.join(ROOT, dst_rel)
    if not os.path.exists(src):
        print(f"  SKIP(없음): {src_rel}")
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        print(f"  FAIL(대상 존재): {dst_rel}")
        return False
    tr = tracked_under(src_rel.replace("\\", "/"))
    if tr:
        # git mv (폴더/파일 모두 지원 — 미추적 파일도 함께 이동됨)
        r = subprocess.run(["git", "mv", src_rel, dst_rel], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            # 폴더에 추적+미추적 혼재 시 git mv 실패 가능 → os 이동 후 git add -A 위임
            os.rename(src, dst)
            print(f"  MV(os·혼재): {src_rel} -> {dst_rel} [추적 {len(tr)}건 — 커밋 시 rename 감지]")
        else:
            print(f"  MV(git): {src_rel} -> {dst_rel} [추적 {len(tr)}건]")
    else:
        os.rename(src, dst)
        print(f"  MV(os): {src_rel} -> {dst_rel}")
    log_move(batch, src_rel, dst_rel)
    return True

def main():
    batch_file, label = sys.argv[1], sys.argv[2]
    ensure_map()
    ok = fail = 0
    for line in io.open(batch_file, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        src, dst = line.split("\t")
        if move(src.strip(), dst.strip(), label):
            ok += 1
        else:
            fail += 1
    print(f"== {label}: 이동 {ok} · 실패/스킵 {fail}")

if __name__ == "__main__":
    main()
