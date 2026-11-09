# Automated validation only: does not start an interactive game window.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    throw 'Python environment missing. Run setup.ps1 first.'
}
$env:SDL_VIDEODRIVER = 'dummy'
$env:SDL_AUDIODRIVER = 'dummy'
$env:PYGAME_HIDE_SUPPORT_PROMPT = '1'
Write-Host 'Step 1/3: Python source and Pygame UI tests' -ForegroundColor Cyan
& $python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Automated tests failed.' }
Write-Host 'Step 2/3: Complete campaign simulation (no human playtime measured)' -ForegroundColor Cyan
& $python tools\simulate_campaign.py
if ($LASTEXITCODE -ne 0) { throw 'Campaign simulation failed.' }
Write-Host 'Step 3/3: Strategy diversity and recipe exploit audit' -ForegroundColor Cyan
& $python tools\stress_test.py
if ($LASTEXITCODE -ne 0) { throw 'Strategy stress test failed.' }
Write-Host 'All available automated checks completed. Human playtime remains unverified.' -ForegroundColor Green
