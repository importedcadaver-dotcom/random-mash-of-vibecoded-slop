# Run from PowerShell in the extracted MudPieMasters folder.
# Creates a venv only when one does not already exist.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Host '[1/3] Creating Python 3.12 virtual environment...'
    py -3.12 -m venv .venv
}
if (-not (Test-Path $python)) { throw 'Python virtual environment was not created.' }
Write-Host '[2/3] Installing runtime and developer dependencies...'
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed.' }
& $python -m pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency install failed.' }
Write-Host '[3/3] Verifying pygame-ce...'
& $python -c "import pygame; print('Pygame CE ready:', pygame.version.ver)"
if ($LASTEXITCODE -ne 0) { throw 'pygame import verification failed.' }
Write-Host 'Ready! Start with .\play.bat or .\run.ps1' -ForegroundColor Green
