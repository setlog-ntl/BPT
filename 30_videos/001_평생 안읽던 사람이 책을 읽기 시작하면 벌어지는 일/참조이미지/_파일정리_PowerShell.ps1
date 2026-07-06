# 다운로드된 23개 이미지를 작업 폴더로 일괄 이동
# 사용법: 이 파일 우클릭 → "PowerShell로 실행" 또는 PowerShell 창에서 실행

$src = "C:\Users\N100274\Downloads"
$dst = "C:\Dev\bizpt\대본\풀링컨텐츠\평생 안읽던 사람이 책을 읽기 시작하면 벌어지는 일\참조이미지"

Write-Host "다운로드 폴더에서 cut_* 파일들을 작업 폴더로 이동합니다..." -ForegroundColor Cyan

# 챕터 00 후크 (4컷)
Write-Host "[챕터 00] cut_00_* 파일 이동..." -ForegroundColor Yellow
Move-Item "$src\cut_00_*.png" "$dst\00_후크_미리보기\" -Force -ErrorAction SilentlyContinue

# 챕터 01 출발점 (6컷 + 중복 1개)
Write-Host "[챕터 01] cut_01_* 파일 이동..." -ForegroundColor Yellow
Move-Item "$src\cut_01_*.png" "$dst\01_출발점_현상\" -Force -ErrorAction SilentlyContinue

# 챕터 03 시야 (13컷)
Write-Host "[챕터 03] cut_03_* 파일 이동..." -ForegroundColor Yellow
Move-Item "$src\cut_03_*.png" "$dst\03_시야_무지개와단어\" -Force -ErrorAction SilentlyContinue

# 결과 확인
Write-Host ""
Write-Host "=== 이동 결과 ===" -ForegroundColor Green
$count00 = (Get-ChildItem "$dst\00_후크_미리보기\cut_*.png").Count
$count01 = (Get-ChildItem "$dst\01_출발점_현상\cut_*.png").Count
$count03 = (Get-ChildItem "$dst\03_시야_무지개와단어\cut_*.png").Count
Write-Host "00_후크_미리보기: $count00 컷"
Write-Host "01_출발점_현상: $count01 컷"
Write-Host "03_시야_무지개와단어: $count03 컷"
Write-Host "총 컷: $($count00 + $count01 + $count03)"

# 다운로드 폴더의 잔여 cut_* 확인
$remaining = (Get-ChildItem "$src\cut_*.png" -ErrorAction SilentlyContinue).Count
if ($remaining -gt 0) {
    Write-Host ""
    Write-Host "[경고] 다운로드 폴더에 $remaining 개의 cut_* 파일이 남아있습니다." -ForegroundColor Red
    Get-ChildItem "$src\cut_*.png" | Select-Object -ExpandProperty Name
} else {
    Write-Host ""
    Write-Host "[완료] 모든 cut_* 파일이 작업 폴더로 정리되었습니다." -ForegroundColor Green
}

Read-Host "Press Enter to close"
