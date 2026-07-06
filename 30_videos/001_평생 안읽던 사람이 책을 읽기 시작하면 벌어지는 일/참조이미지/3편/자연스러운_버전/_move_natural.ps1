$ErrorActionPreference = "Continue"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$srcDir = Join-Path $env:USERPROFILE "Downloads"
$dstDir = $PSScriptRoot
Write-Host "Source: $srcDir"
Write-Host "Destination: $dstDir"
Write-Host ""

# Map each chatgpt_3pyeon_natural_XX.png to a meaningful natural-doc cut filename
$mappings = @(
    @{ src = "chatgpt_3pyeon_natural_01.png"; dst = "natural_01_cafe_book_morning.png" },
    @{ src = "chatgpt_3pyeon_natural_02.png"; dst = "natural_02_window_reader_silhouette.png" },
    @{ src = "chatgpt_3pyeon_natural_03.png"; dst = "natural_03_home_bookshelf.png" },
    @{ src = "chatgpt_3pyeon_natural_04.png"; dst = "natural_04_dawn_path_mountains.png" },
    @{ src = "chatgpt_3pyeon_natural_05.png"; dst = "natural_05_elderly_hands_page.png" },
    @{ src = "chatgpt_3pyeon_natural_06.png"; dst = "natural_06_pond_ripple_macro.png" },
    @{ src = "chatgpt_3pyeon_natural_07.png"; dst = "natural_07_tree_roots_forest.png" },
    @{ src = "chatgpt_3pyeon_natural_08.png"; dst = "natural_08_autumn_path.png" },
    @{ src = "chatgpt_3pyeon_natural_09.png"; dst = "natural_09_one_word_note.png" },
    @{ src = "chatgpt_3pyeon_natural_10.png"; dst = "natural_10_library_nook.png" },
    @{ src = "chatgpt_3pyeon_natural_11.png"; dst = "natural_11_tabbed_book.png" },
    @{ src = "chatgpt_3pyeon_natural_12.png"; dst = "natural_12_balcony_morning.png" },
    @{ src = "chatgpt_3pyeon_natural_13.png"; dst = "natural_13_journal_dried_flowers.png" },
    @{ src = "chatgpt_3pyeon_natural_14.png"; dst = "natural_14_sprout_in_pot.png" },
    @{ src = "chatgpt_3pyeon_natural_15.png"; dst = "natural_15_mountain_sunrise.png" },
    @{ src = "chatgpt_3pyeon_natural_16.png"; dst = "natural_16_underline_with_pencil.png" },
    @{ src = "chatgpt_3pyeon_natural_17.png"; dst = "natural_17_tea_and_book.png" },
    @{ src = "chatgpt_3pyeon_natural_18.png"; dst = "natural_18_golden_grass_field.png" },
    @{ src = "chatgpt_3pyeon_natural_19.png"; dst = "natural_19_evening_diary_candle.png" },
    @{ src = "chatgpt_3pyeon_natural_20.png"; dst = "natural_20_page_turn_cozy_home.png" }
)

$moved = 0
$skipped = 0
foreach ($m in $mappings) {
    $srcPath = Join-Path $srcDir $m.src
    if (Test-Path -LiteralPath $srcPath) {
        $dstPath = Join-Path $dstDir $m.dst
        Move-Item -LiteralPath $srcPath -Destination $dstPath -Force
        Write-Host "MOVED: $($m.src) -> $($m.dst)"
        $moved++
    } else {
        Write-Host "SKIP (not found): $($m.src)"
        $skipped++
    }
}

Write-Host ""
Write-Host "=== Moved: $moved, Skipped: $skipped ==="
Write-Host ""
Write-Host "Final state of 자연스러운_버전:"
Get-ChildItem -LiteralPath $dstDir -File -Filter "natural_*.png" | Sort-Object Name | ForEach-Object {
    Write-Host "  $($_.Name) ($([math]::Round($_.Length/1024)) KB)"
}
Write-Host ""
Write-Host "Total natural_*.png: $((Get-ChildItem -LiteralPath $dstDir -File -Filter 'natural_*.png').Count)"
Start-Sleep -Seconds 10
