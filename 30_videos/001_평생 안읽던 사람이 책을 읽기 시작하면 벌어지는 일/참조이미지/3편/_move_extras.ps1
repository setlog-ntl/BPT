$ErrorActionPreference = "Continue"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$srcDir = Join-Path $env:USERPROFILE "Downloads"
$dstDir = $PSScriptRoot
$newBatch = Get-ChildItem -Path $srcDir -Filter "chatgpt_3pyeon_extra_*.png" -ErrorAction SilentlyContinue | Sort-Object Name
foreach ($f in $newBatch) {
    $dstPath = Join-Path $dstDir $f.Name
    if (-not (Test-Path -LiteralPath $dstPath)) {
        Move-Item -LiteralPath $f.FullName -Destination $dstPath -Force
        Write-Host "MOVED: $($f.Name)"
    }
}
Write-Host "Done. Total PNG: $((Get-ChildItem -LiteralPath $dstDir -File -Filter '*.png').Count)"
Start-Sleep -Seconds 5
