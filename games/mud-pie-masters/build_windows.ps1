# Build on Windows; resulting standalone executable appears in dist\.
$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { throw 'Run setup.ps1 first.' }
& $python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name MudPieMasters --add-data 'assets;assets' main.py
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed.' }
Write-Host 'Build created: dist\MudPieMasters.exe' -ForegroundColor Green
Write-Host 'Please LAUNCH and playtest the EXE before treating it as a verified release.'
