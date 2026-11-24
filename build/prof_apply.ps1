# Professor pass: apply one lesson's changes and render review sheets.  .\prof_apply.ps1 L01
param([string]$L)
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot
$f = (Get-ChildItem "lessons\$($L)_*.py").FullName
if (Test-Path "prof_blocks\$($L)_pairs.py") { & python -P -E repl.py $f "prof_blocks\$($L)_pairs.py" }
if (Test-Path "prof_blocks\$L.py") { & python -P -E append.py $f "prof_blocks\$L.py" }
& python -P -E build2.py --only $L --frames 2>&1 | Select-Object -Last 3
& python -P -E prof_sheet.py $L
& python -P -E watch.py $L > "prof\$($L)_new.txt"
