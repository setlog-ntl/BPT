param([switch]$Force)
$DownloadDir = "$env:USERPROFILE\Downloads"
$RefImageRoot = "C:\Dev\bizpt\대본\풀링컨텐츠\평생 안읽던 사람이 책을 읽기 시작하면 벌어지는 일\참조이미지"
$Chapter04Dir = Join-Path $RefImageRoot "04_사고_프레임_더닝크루거_정점사람들"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Move existing duplicate cut_04-03 to recovery
$existingWisdomCard = Join-Path $Chapter04Dir "cut_04-03_wisdom_quote_card.png"
$recoveryDir = Join-Path $RefImageRoot "_복원_잘못된_매핑"
if (Test-Path $existingWisdomCard) {
    if (-not (Test-Path $recoveryDir)) { New-Item -ItemType Directory -Path $recoveryDir -Force | Out-Null }
    Move-Item -Path $existingWisdomCard -Destination (Join-Path $recoveryDir "cut_04-03_wisdom_quote_card_DUPLICATE.png") -Force
    Write-Host "Moved duplicate cut_04-03 to recovery" -ForegroundColor Yellow
}

# Find the small wisdom card files (under 800KB) in Downloads from tonight
$cutoff = (Get-Date).AddMinutes(-180)
$candidates = Get-ChildItem -Path $DownloadDir -Filter "ChatGPT Image*.png" -File |
              Where-Object { $_.LastWriteTime -ge $cutoff -and ($_.Length / 1KB) -lt 800 -and ($_.Length / 1KB) -gt 100 } |
              Sort-Object LastWriteTime

Write-Host "Candidate wisdom card files (small, recent):"
foreach ($f in $candidates) {
    $sizeKB = [Math]::Round($f.Length / 1KB)
    Write-Host ("  " + $f.Name + " (" + $sizeKB + " KB)") -ForegroundColor Gray
}
Write-Host ""

if ($candidates.Count -eq 0) {
    Write-Host "No small wisdom card candidate found." -ForegroundColor Red
    exit
}

# Take the LATEST small file as the wisdom card (the second generation if there are duplicates)
$wisdomCard = $candidates[-1]
$destPath = Join-Path $Chapter04Dir "cut_04-03_wisdom_quote_card.png"

Write-Host ("Moving wisdom card: " + $wisdomCard.Name + " -> cut_04-03_wisdom_quote_card.png") -ForegroundColor Cyan

if (-not $Force) {
    $c = Read-Host "Proceed? (y/N)"
    if ($c -ne "y" -and $c -ne "Y") { exit }
}

Move-Item -Path $wisdomCard.FullName -Destination $destPath -Force
Write-Host "Done." -ForegroundColor Green
