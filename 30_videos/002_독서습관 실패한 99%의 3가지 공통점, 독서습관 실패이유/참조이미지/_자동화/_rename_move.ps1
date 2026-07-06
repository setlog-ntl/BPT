<#
  _rename_move.ps1  (무문구 비주얼 47컷판)
  ChatGPT(DALL·E)에서 받은 이미지를 다운로드 순서대로 각 챕터 폴더의 지정 파일명으로 이동.
  사용:
    .\_rename_move.ps1 -DryRun                 # 미리보기
    .\_rename_move.ps1 -Force                   # 실제 실행
    .\_rename_move.ps1 -Force -SinceMinutes 120 # 최근 120분 내 받은 것만
    .\_rename_move.ps1 -Force -StartIndex 6     # 6번 컷부터(중간 재실행)
  매핑 순서는 ChatGPT_입력순서.md 의 1~47번과 동일해야 합니다.
#>
param(
  [switch]$DryRun, [switch]$Force,
  [int]$StartIndex = 1, [int]$SinceMinutes = 0,
  [string]$DownloadDir = "$env:USERPROFILE\Downloads"
)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Root = Split-Path -Parent $PSScriptRoot
Write-Host "참조이미지 루트: $Root" -ForegroundColor Cyan

$Map = @(
  "00_후크_미리보기\cut_00-01_unread_book_tower.png",
  "00_후크_미리보기\cut_00-02_tiny_person_giant_book.png",
  "00_후크_미리보기\cut_00-03_open_book_trap.png",
  "00_후크_미리보기\cut_00-04_fingers_count_123.png",
  "00_후크_미리보기\cut_00-05_closed_vs_half_book.png",
  "01_두번의_실패담\cut_01-01_pick_brick_book.png",
  "01_두번의_실패담\cut_01-02_drowsy_blur_page.png",
  "01_두번의_실패담\cut_01-03_dusty_abandoned_book.png",
  "01_두번의_실패담\cut_01-04_gift_cosmos_book.png",
  "01_두번의_실패담\cut_01-05_friend_walks_away.png",
  "02_면죄부_안읽히는건당연\cut_02-01_warm_palm_light.png",
  "02_면죄부_안읽히는건당연\cut_02-02_fog_dissolving_text.png",
  "02_면죄부_안읽히는건당연\cut_02-03_foreign_script_book.png",
  "02_면죄부_안읽히는건당연\cut_02-04_barbell_empty_hands.png",
  "02_면죄부_안읽히는건당연\cut_02-05_sapling_from_book.png",
  "03_공통점1_명저부터편다\cut_03-01_four_brick_books.png",
  "03_공통점1_명저부터편다\cut_03-02_huge_vs_small_book.png",
  "03_공통점1_명저부터편다\cut_03-03_finish_thin_book.png",
  "03_공통점1_명저부터편다\cut_03-04_controller_down.png",
  "03_공통점1_명저부터편다\cut_03-05_first_page_crumbling.png",
  "04_공통점2_자기를탓한다\cut_04-01_blame_silhouette.png",
  "04_공통점2_자기를탓한다\cut_04-02_defeated_hand.png",
  "04_공통점2_자기를탓한다\cut_04-03_red_stamp_mark.png",
  "04_공통점2_자기를탓한다\cut_04-04_tenyears_cobweb.png",
  "04_공통점2_자기를탓한다\cut_04-05_small_hand_big_weight.png",
  "05_공통점3_읽어야할것같은책\cut_05-01_want_vs_should_book.png",
  "05_공통점3_읽어야할것같은책\cut_05-02_immersed_vs_bored.png",
  "05_공통점3_읽어야할것같은책\cut_05-03_stone_iron_book.png",
  "05_공통점3_읽어야할것같은책\cut_05-04_untouched_cosmos.png",
  "05_공통점3_읽어야할것같은책\cut_05-05_postponed_book.png",
  "06_해결_3기준과4년뒤\cut_06-01_brightening_desk.png",
  "06_해결_3기준과4년뒤\cut_06-02_three_symbol_books.png",
  "06_해결_3기준과4년뒤\cut_06-03_light_thin_book.png",
  "06_해결_3기준과4년뒤\cut_06-04_thin_finish_vs_brick.png",
  "06_해결_3기준과4년뒤\cut_06-05_one_line_light.png",
  "06_해결_3기준과4년뒤\cut_06-06_brick_book_half.png",
  "07_결호명_CTA\cut_07-01_hands_rest_warm.png",
  "07_결호명_CTA\cut_07-02_pick_thin_book.png",
  "07_결호명_CTA\cut_07-03_side_by_side_reading.png",
  "07_결호명_CTA\cut_07-04_book_to_tree.png",
  "07_결호명_CTA\cut_07-05_empty_chair_invite.png",
  "EXTRAS_브롤\cut_EX-01_page_turn_loop.png",
  "EXTRAS_브롤\cut_EX-02_bookshelf_track.png",
  "EXTRAS_브롤\cut_EX-03_reading_nook_chair.png",
  "EXTRAS_브롤\cut_EX-04_dust_beam.png",
  "EXTRAS_브롤\cut_EX-05_time_passing_pages.png",
  "EXTRAS_브롤\cut_EX-06_thumbnail_base.png"
)

if (-not $DryRun -and -not $Force) { Write-Host "`n-DryRun 또는 -Force 를 지정하세요." -ForegroundColor Yellow; return }

$files = Get-ChildItem -Path $DownloadDir -Filter *.png -File -ErrorAction SilentlyContinue
if ($SinceMinutes -gt 0) { $cut=(Get-Date).AddMinutes(-$SinceMinutes); $files=$files|Where-Object{$_.LastWriteTime -ge $cut} }
$downloads = $files | Sort-Object LastWriteTime
if (-not $downloads) { Write-Host "다운로드 png 없음: $DownloadDir" -ForegroundColor Red; return }
Write-Host "수집 $($downloads.Count)개 / 슬롯 $($Map.Count)개`n" -ForegroundColor Cyan

$idx = $StartIndex - 1; $used = 0
foreach ($src in $downloads) {
  if ($idx -ge $Map.Count) { break }
  $rel = $Map[$idx]
  $destDir = Join-Path $Root (Split-Path -Parent $rel)
  $dest = Join-Path $destDir (Split-Path -Leaf $rel)
  if (Test-Path $dest) {
    $b=[IO.Path]::GetFileNameWithoutExtension($dest); $e=[IO.Path]::GetExtension($dest); $n=1
    while (Test-Path (Join-Path $destDir "$b($n)$e")) { $n++ }
    $dest = Join-Path $destDir "$b($n)$e"
  }
  $tag = "[{0,2}] {1} -> {2}" -f ($idx+1), $src.Name, $rel
  if ($DryRun) { Write-Host "DRY  $tag" -ForegroundColor DarkGray }
  else { if(-not(Test-Path $destDir)){New-Item -ItemType Directory -Path $destDir -Force|Out-Null}; Move-Item -LiteralPath $src.FullName -Destination $dest -Force; Write-Host "MOVE $tag" -ForegroundColor Green }
  $idx++; $used++
}
Write-Host "`n완료: $used개 (시작 $StartIndex)." -ForegroundColor Cyan
if ($DryRun) { Write-Host "※ 미리보기. 실제 이동은 -Force." -ForegroundColor Yellow }
