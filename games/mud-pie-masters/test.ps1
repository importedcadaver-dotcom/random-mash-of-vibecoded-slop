$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { throw 'Run setup.ps1 first.' }
# Unit tests and virtual-display graphical smoke tests (SDL dummy).
$env:SDL_VIDEODRIVER='dummy'
$env:SDL_AUDIODRIVER='dummy'
& $python -m pytest -v
exit $LASTEXITCODE
