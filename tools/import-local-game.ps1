# Imports the v0.5 project into ONLY games/mud-pie-masters, without touching other games.
# Run from a clone of the dedicated ChatGPT branch, with a ZIP downloaded locally from ChatGPT.
param(
  [string]$ZipPath = "$HOME\Downloads\MudPieMasters-v0.5.0.zip",
  [switch]$CommitAndPush
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Branch = 'agents/chatgpt-gpt6/mud-pie-masters-import-20261108'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git not found. Install Git for Windows first.' }
if (-not (Test-Path (Join-Path $Repo '.git'))) { throw 'Run inside a Git clone of the monorepo.' }
if (-not (Test-Path -LiteralPath $ZipPath)) { throw "Cannot find $ZipPath. Download v0.5 ZIP to your Downloads folder first." }
$CurrentBranch = (git -C $Repo branch --show-current).Trim()
if ($CurrentBranch -ne $Branch) { throw "Switch to $Branch first. Current: $CurrentBranch" }
$Dirty = @(git -C $Repo status --porcelain)
if ($Dirty.Count -gt 0) { throw 'Working tree is not clean. Commit or stash changes before import.' }
$Temp = Join-Path ([IO.Path]::GetTempPath()) ("mudpie-import-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $Temp -Force | Out-Null
try {
  Expand-Archive -LiteralPath $ZipPath -DestinationPath $Temp -Force
  $Source = $Temp
  if (-not (Test-Path (Join-Path $Source 'main.py'))) {
    $Candidates = @(Get-ChildItem -LiteralPath $Temp -Directory)
    if ($Candidates.Count -eq 1 -and (Test-Path (Join-Path $Candidates[0].FullName 'main.py'))) {
      $Source = $Candidates[0].FullName
    }
  }
  foreach ($Required in @('main.py','mudpie/models.py','mudpie/game.py','tests/test_models.py','assets/player.png')) {
    if (-not (Test-Path (Join-Path $Source $Required))) { throw "ZIP missing expected game file: $Required" }
  }
  $Dest = Join-Path $Repo 'games\mud-pie-masters'
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
  $Files = @(Get-ChildItem -LiteralPath $Source -Recurse -File | Where-Object {
    $_.FullName -notmatch '[\\/](\.venv|__pycache__|\.pytest_cache|\.ruff_cache|build|dist)[\\/]' -and
    $_.Name -notmatch '\.(pyc|pyo)$'
  })
  foreach ($File in $Files) {
    $Relative = $File.FullName.Substring($Source.Length).TrimStart('\','/')
    if ($Relative -in @('AGENTS.md','game.json')) { continue }
    $Target = Join-Path $Dest $Relative
    $Parent = Split-Path $Target -Parent
    New-Item -ItemType Directory -Force -Path $Parent | Out-Null
    Copy-Item -LiteralPath $File.FullName -Destination $Target -Force
  }
  & git -C $Repo add -- 'games/mud-pie-masters'
  if ($LASTEXITCODE -ne 0) { throw 'git add failed' }
  Write-Host ("Prepared {0} project files for commit." -f $Files.Count)
  & git -C $Repo diff --cached --stat
  if ($CommitAndPush) {
    & git -C $Repo commit -m "[ChatGPT GPT-6 / mud-pie-masters] Import complete v0.5 source and original assets"
    if ($LASTEXITCODE -ne 0) { throw 'git commit failed' }
    & git -C $Repo push -u origin $Branch
    if ($LASTEXITCODE -ne 0) { throw 'Push failed; check GitHub authentication and remote permission' }
    Write-Host 'Pushed Mud Pie Masters source to the dedicated pull request branch.'
  } else {
    Write-Host 'Imported into staging. Review the diff, then run git commit and push, or rerun with -CommitAndPush.'
  }
}
finally {
  if (Test-Path $Temp) { Remove-Item -LiteralPath $Temp -Recurse -Force }
}
