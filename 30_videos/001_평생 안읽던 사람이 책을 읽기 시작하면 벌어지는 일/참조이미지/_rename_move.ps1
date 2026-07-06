# 캡션 기반 이미지 자동 리네임/이동 스크립트
param(
    [int]$SinceMinutes = 1440,
    [int]$StartIndex   = 1,
    [int]$MinSizeKB    = 800,
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$DownloadDir   = "$env:USERPROFILE\Downloads"
$RefImageRoot  = "C:\Dev\bizpt\대본\풀링컨텐츠\평생 안읽던 사람이 책을 읽기 시작하면 벌어지는 일\참조이미지"

$Mapping = @(
    @{ idx=1;  slug="cut_04-01_ripple_droplet.png";        sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=2;  slug="cut_04-02_frame_book.png";             sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=3;  slug="cut_04-03_wisdom_quote_card.png";      sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=4;  slug="cut_04-08_book_mountain_peak.png";     sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ idx=5;  slug="cut_05-03_golden_footprint.png";       sub="05_성장_뇌근육_그럼에도" },
    @{ idx=6;  slug="cut_06-01_3axis_triptych.png";         sub="06_결호명" },
    @{ idx=7;  slug="cut_07-02_subscribe_icons.png";        sub="07_CTA" },
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

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "=== Caption Image Auto-Organize ===" -ForegroundColor Cyan
Write-Host ("Downloads      : " + $DownloadDir)
Write-Host ("RefImage Root  : " + $RefImageRoot)
Write-Host ("Filter         : last $SinceMinutes min, min ${MinSizeKB}KB")
Write-Host ("Start Index    : $StartIndex")
if ($DryRun) { Write-Host "MODE: DRY-RUN" -ForegroundColor Yellow }
if ($Force)  { Write-Host "MODE: FORCE (no confirm)" -ForegroundColor Yellow }
Write-Host ""

$cutoff = (Get-Date).AddMinutes(-$SinceMinutes)
$files = @()
$files += Get-ChildItem -Path $DownloadDir -Filter "ChatGPT Image*.png" -File -ErrorAction SilentlyContinue
$files += Get-ChildItem -Path $DownloadDir -Filter "cut_*.png" -File -ErrorAction SilentlyContinue
$files = $files | Where-Object { $_.LastWriteTime -ge $cutoff -and ($_.Length / 1KB) -ge $MinSizeKB } | Sort-Object LastWriteTime -Unique

if ($files.Count -eq 0) {
    Write-Host "No matching files in Downloads." -ForegroundColor Yellow
    exit
}

Write-Host ("Found: " + $files.Count + " files") -ForegroundColor Green
Write-Host ""

$mapStart = $StartIndex - 1
if ($mapStart -ge $Mapping.Count) {
    Write-Host "StartIndex exceeds mapping range" -ForegroundColor Red
    exit
}
$processCount = [Math]::Min($files.Count, $Mapping.Count - $mapStart)

Write-Host "Mapping:" -ForegroundColor Cyan
for ($i = 0; $i -lt $processCount; $i++) {
    $f = $files[$i]
    $m = $Mapping[$mapStart + $i]
    $sizeKB = [Math]::Round($f.Length / 1KB)
    Write-Host ("  [{0,2}] {1,-55} {2,5}KB" -f $m.idx, $f.Name, $sizeKB)
    Write-Host ("       -> " + $m.sub + "\" + $m.slug) -ForegroundColor DarkGray
}
Write-Host ""

if ($DryRun) { exit }

if (-not $Force) {
    $confirm = Read-Host "Proceed? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") { Write-Host "Cancelled."; exit }
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

    $finalDest = $dest
    $n = 1
    while (Test-Path $finalDest) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($dest)
        $ext  = [System.IO.Path]::GetExtension($dest)
        $finalDest = Join-Path $destDir ($base + "(" + $n + ")" + $ext)
        $n++
    }

    try {
        Move-Item -Path $src -Destination $finalDest -Force
        Write-Host ("  OK  " + (Split-Path $src -Leaf) + " -> " + (Split-Path $finalDest -Leaf)) -ForegroundColor Green
        $moved++
    } catch {
        Write-Host ("  ERR " + $_) -ForegroundColor Red
        $skipped++
    }
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
Write-Host ("Moved: $moved / Failed: $skipped") -ForegroundColor Green
