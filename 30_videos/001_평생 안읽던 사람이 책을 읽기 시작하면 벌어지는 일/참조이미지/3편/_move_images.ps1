$ErrorActionPreference = "Continue"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$srcDir = Join-Path $env:USERPROFILE "Downloads"
$dstDir = $PSScriptRoot
Write-Host "Source: $srcDir"
Write-Host "Destination: $dstDir"
Write-Host ""

# Get all chatgpt_3pyeon_full_XX.png files in Downloads (the new batch from this session)
$newBatch = Get-ChildItem -Path $srcDir -Filter "chatgpt_3pyeon_full_*.png" -ErrorAction SilentlyContinue | Sort-Object Name

Write-Host "Found $($newBatch.Count) new chatgpt_3pyeon_full_*.png files to organize"
Write-Host ""

# Move each to 3편 folder, preserving the chatgpt_3pyeon_full_XX naming so user can review and rename
$moved = 0
foreach ($f in $newBatch) {
    $dstPath = Join-Path $dstDir $f.Name
    if (-not (Test-Path -LiteralPath $dstPath)) {
        Move-Item -LiteralPath $f.FullName -Destination $dstPath -Force
        Write-Host "MOVED: $($f.Name)"
        $moved++
    } else {
        # If file already exists at dst, leave src alone
        Write-Host "SKIP (already exists in dst): $($f.Name)"
    }
}

Write-Host ""
Write-Host "=== Moved $moved files ==="
Write-Host ""
Write-Host "All image files in 3편:"
Get-ChildItem -LiteralPath $dstDir -File -Filter "*.png" | Sort-Object Name | ForEach-Object {
    Write-Host "  $($_.Name) ($([math]::Round($_.Length/1024)) KB)"
}
Write-Host ""
Write-Host "Total PNG files: $((Get-ChildItem -LiteralPath $dstDir -File -Filter '*.png').Count)"
Start-Sleep -Seconds 15
