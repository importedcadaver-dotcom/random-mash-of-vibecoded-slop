$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Host 'Missing Python environment. Run: powershell -ExecutionPolicy Bypass -File .\setup.ps1' -ForegroundColor Yellow
    exit 1
}
& $python main.py
exit $LASTEXITCODE
