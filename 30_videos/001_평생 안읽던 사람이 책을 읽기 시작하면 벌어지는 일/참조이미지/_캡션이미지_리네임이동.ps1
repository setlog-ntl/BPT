# =====================================================================
# 캡션 기반 이미지 자동 리네임/이동 스크립트
# =====================================================================
# 사용법:
#   cd "C:\Dev\bizpt\대본\풀링컨텐츠\평생 안읽던 사람이 책을 읽기 시작하면 벌어지는 일\참조이미지"
#   .\_캡션이미지_리네임이동.ps1                # 대화형
#   .\_캡션이미지_리네임이동.ps1 -DryRun        # 미리보기
#   .\_캡션이미지_리네임이동.ps1 -Force         # 확인 없이 즉시 실행
#   .\_캡션이미지_리네임이동.ps1 -StartIndex 8  # 8번부터 이어서
# =====================================================================
param(
    [int]$SinceMinutes = 1440,    # 기본 24시간
    [int]$StartIndex   = 1,
    [int]$MinSizeKB    = 800,     # 작은 썸네일/실패 파일 제외 (KB)
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$DownloadDir   = "$env:USERPROFILE\Downloads"
$RefImageRoot  = "C:\Dev\bizpt\대본\풀링컨텐츠\평생 안읽던 사람이 책을 읽기 시작하면 벌어지는 일\참조이미지"

# 매핑 (이번 세션 생성 순서대로)
# 1~7: ChatGPT 자동화로 생성 완료 / 8~25: 사용자가 .md 파일 순서대로 추가 생성 예정
$Mapping = @(
    @{ idx=1;  slug="cut_04-01_ripple_droplet.png";        sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=2;  slug="cut_04-02_frame_book.png";             sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=3;  slug="cut_04-03_wisdom_quote_card.png";      sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=4;  slug="cut_04-08_book_mountain_peak.png";     sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=5;  slug="cut_05-03_golden_footprint.png";       sub="05_성장_뇌근육_그럼에도" },
    @{ idx=6;  slug="cut_06-01_3axis_triptych.png";         sub="06_결호명" },
    @{ idx=7;  slug="cut_07-02_subscribe_icons.png";        sub="07_CTA" },
    # --- 8번부터 사용자 추가 생성 (.md 파일 순서) ---
    @{ idx=8;  slug="cut_04-04_smart_vs_wisdom.png";        sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=9;  slug="cut_04-05_window_room.png";            sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=10; slug="cut_04-06_tinted_glass.png";           sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=11; slug="cut_04-07_dunning_kruger_curve.png";   sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=12; slug="cut_04-09_stream_forest.png";          sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=13; slug="cut_04-10_esports_book.png";           sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=14; slug="cut_04-11_many_windows.png";           sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=15; slug="cut_05-01_dim_room_book.png";          sub="05_성장_뇌근육_그럼에도" },
    @{ idx=16; slug="cut_05-02_stone_stair_descent.png";    sub="05_성장_뇌근육_그럼에도" },
    @{ idx=17; slug="cut_05-04_now_vs_10years.png";         sub="05_성장_뇌근육_그럼에도" },
    @{ idx=18; slug="cut_05-05_elderly_hands_book.png";     sub="05_성장_뇌근육_그럼에도" },
    @{ idx=19; slug="cut_05-06_dusty_dumbbell.png";         sub="05_성장_뇌근육_그럼에도" },
    @{ idx=20; slug="cut_05-07_track_start_finish.png";     sub="05_성장_뇌근육_그럼에도" },
    @{ idx=21; slug="cut_05-08_moving_walkway.png";         sub="05_성장_뇌근육_그럼에도" },
    @{ idx=22; slug="cut_05-09_circled_word_page.png";      sub="05_성장_뇌근육_그럼에도" },
    @{ idx=23; slug="cut_06-02_first_page_open.png";        sub="06_결호명" },
    @{ idx=24; slug="cut_06-03_three_groups_card.png";      sub="06_결호명" },
    @{ idx=25; slug="cut_07-01_desk_reading_tools.png";     sub="07_CTA" }
)

# 한글 콘솔 출력
try { $OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "=== 캡션 이미지 자동 정리 ===" -ForegroundColor Cyan
Write-Host "Downloads      : $DownloadDir"
Write-Host "참조이미지 폴더 : $RefImageRoot"
Write-Host "필터            : 최근 ${SinceMinutes}분, 최소 ${MinSizeKB}KB"
Write-Host "시작 인덱스     : $StartIndex"
if ($DryRun) { Write-Host "MODE           : DRY-RUN" -ForegroundColor Yellow }
if ($Force)  { Write-Host "MODE           : FORCE (확인 없음)" -ForegroundColor Yellow }
Write-Host ""

# 파일 수집: ChatGPT Image*.png + cut_*.png (커스텀 이름)
$cutoff = (Get-Date).AddMinutes(-$SinceMinutes)
$files = @()
$files += Get-ChildItem -Path $DownloadDir -Filter "ChatGPT Image*.png" -File -ErrorAction SilentlyContinue
$files += Get-ChildItem -Path $DownloadDir -Filter "cut_*.png" -File -ErrorAction SilentlyContinue
$files = $files |
         Where-Object { $_.LastWriteTime -ge $cutoff -and ($_.Length / 1KB) -ge $MinSizeKB } |
         Sort-Object LastWriteTime -Unique

if ($files.Count -eq 0) {
    Write-Host "조건에 맞는 이미지가 없습니다." -ForegroundColor Yellow
    Write-Host "TIP: -SinceMinutes 또는 -MinSizeKB를 조정해 보세요."
    exit
}

Write-Host "발견된 이미지: $($files.Count)개" -ForegroundColor Green
Write-Host ""

$mapStart = $StartIndex - 1
if ($mapStart -ge $Mapping.Count) {
    Write-Host "StartIndex가 매핑 범위($($Mapping.Count))를 초과했습니다." -ForegroundColor Red
    exit
}
$processCount = [Math]::Min($files.Count, $Mapping.Count - $mapStart)

Write-Host "매핑 (오래된 다운로드 = 작은 인덱스):" -ForegroundColor Cyan
for ($i = 0; $i -lt $processCount; $i++) {
    $f = $files[$i]
    $m = $Mapping[$mapStart + $i]
    $sizeKB = [Math]::Round($f.Length / 1KB)
    Write-Host ("  [{0,2}] {1,-55} {2,5}KB  {3}" -f $m.idx, $f.Name, $sizeKB, $f.LastWriteTime.ToString("MM-dd HH:mm"))
    Write-Host ("       -> {0}\{1}" -f $m.sub, $m.slug) -ForegroundColor DarkGray
}
Write-Host ""

if ($DryRun) {
    Write-Host "DRY-RUN 종료. 실제 이동하려면 -DryRun 옵션을 제거하세요." -ForegroundColor Yellow
    exit
}

if (-not $Force) {
    $confirm = Read-Host "위 매핑대로 진행할까요? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "취소됨." -ForegroundColor Yellow
        exit
    }
}

$moved = 0; $skipped = 0
for ($i = 0; $i -lt $processCount; $i++) {
    $src = $files[$i].FullName
    $m = $Mapping[$mapStart + $i]
    $destDir = Join-Path $RefImageRoot $m.sub
    $dest = Join-Path $destDir $m.slug

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    # 충돌 회피
    $finalDest = $dest
    $n = 1
    while (Test-Path $finalDest) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($dest)
        $ext  = [System.IO.Path]::GetExtension($dest)
        $finalDest = Join-Path $destDir "$base($n)$ext"
        $n++
    }

    try {
        Move-Item -Path $src -Destination $finalDest -Force
        Write-Host ("  OK  {0,-50} -> {1}" -f (Split-Path $src -Leaf), (Split-Path $finalDest -Leaf)) -ForegroundColor Green
        $moved++
    } catch {
        Write-Host ("  ERR {0}: {1}" -f $src, $_) -ForegroundColor Red
        $skipped++
    }
}

Write-Host ""
Write-Host "=== 완료 ===" -ForegroundColor Cyan
Write-Host ("이동 성공: {0}개 / 실패: {1}개" -f $moved, $skipped) -ForegroundColor Green
Write-Host ""
Write-Host "남은 18개 이미지 생성 후 다시 실행하면 자동으로 8번 인덱스부터 이어서 처리됩니다."
Write-Host "(이미 처리된 파일은 Downloads에서 빠지므로 자연스럽게 다음 묶음이 잡힙니다.)"
