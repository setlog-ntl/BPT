param([switch]$DryRun, [switch]$Force)
$DownloadDir = "$env:USERPROFILE\Downloads"
$RefImageRoot = "C:\Dev\bizpt\대본\풀링컨텐츠\평생 안읽던 사람이 책을 읽기 시작하면 벌어지는 일\참조이미지"

# Mapping for tonight's 7 generated images (in time order)
# Image 1 (ripple) is already moved; check size to filter
$Mapping = @(
    @{ slug="cut_04-02_frame_book.png";          sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ slug="cut_04-03_wisdom_quote_card.png";   sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ slug="cut_04-08_book_mountain_peak.png";  sub="04_사고_프레임_더닝크루거_정점사람들" },
    @{ slug="cut_05-03_golden_footprint.png";    sub="05_성장_뇌근육_그럼에도" },
    @{ slug="cut_06-01_3axis_triptych.png";      sub="06_결호명" },
    @{ slug="cut_07-02_subscribe_icons.png";     sub="07_CTA" }
)

# Get only tonight's images (last 120 min), min 1MB to skip junk thumbnails
$cutoff = (Get-Date).AddMinutes(-120)
$files = Get-ChildItem -Path $DownloadDir -Filter "ChatGPT Image*.png" -File |
         Where-Object { $_.LastWriteTime -ge $cutoff -and ($_.Length / 1KB) -ge 1000 } |
         Sort-Object LastWriteTime |
         Select-Object -Skip 1   # Skip first one (assumed to be duplicate of 04-01 ripple)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host ""
Write-Host "=== Tonight Image Mapping (skip first = ripple duplicate) ===" -ForegroundColor Cyan
Write-Host "Found: $($files.Count) candidate files"
Write-Host ""

$processCount = [Math]::Min($files.Count, $Mapping.Count)
for ($i = 0; $i -lt $processCount; $i++) {
    $f = $files[$i]
    $m = $Mapping[$i]
    $sizeKB = [Math]::Round($f.Length / 1KB)
    Write-Host ("  [{0}] {1} ({2}KB) -> {3}\{4}" -f ($i+1), $f.Name, $sizeKB, $m.sub, $m.slug)
}
Write-Host ""

if ($DryRun) { Write-Host "DRY-RUN. Use -Force to actually move."; exit }
if (-not $Force) {
    $c = Read-Host "Proceed? (y/N)"
    if ($c -ne "y" -and $c -ne "Y") { exit }
}

$moved=0; $errs=0
for ($i = 0; $i -lt $processCount; $i++) {
    $f = $files[$i]
    $m = $Mapping[$i]
    $destDir = Join-Path $RefImageRoot $m.sub
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    $dest = Join-Path $destDir $m.slug
    $finalDest = $dest
    $n = 1
    while (Test-Path $finalDest) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($dest)
        $ext  = [System.IO.Path]::GetExtension($dest)
        $finalDest = Join-Path $destDir ($base + "(" + $n + ")" + $ext)
        $n++
    }
    try {
        Move-Item -Path $f.FullName -Destination $finalDest -Force
        Write-Host ("  OK  " + $f.Name + " -> " + (Split-Path $finalDest -Leaf)) -ForegroundColor Green
        $moved++
    } catch {
        Write-Host ("  ERR " + $_) -ForegroundColor Red
        $errs++
    }
}
Write-Host ""
Write-Host ("=== Done: $moved moved, $errs errors ===") -ForegroundColor Cyan
