param([string]$Url = 'http://127.0.0.1:8790/?local=1&selftest=1')
$w = $PSScriptRoot
$rep = "$w\server\selftest_report.json"
$ud = "$w\edge_prof"
Remove-Item $rep -ErrorAction SilentlyContinue
$a = @('--headless=new', '--inprivate', '--disable-sync', '--no-first-run', '--disable-extensions', '--disable-gpu',
       '--autoplay-policy=no-user-gesture-required', '--mute-audio',
       '--disable-background-media-suspend', '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--disable-backgrounding-occluded-windows',
       "--user-data-dir=$ud", $Url)
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList $a | Out-Null
$sw = [Diagnostics.Stopwatch]::StartNew()
while (-not (Test-Path $rep) -and $sw.Elapsed.TotalMinutes -lt 40) { Start-Sleep 5 }
"elapsed {0:N0}s report={1}" -f $sw.Elapsed.TotalSeconds, (Test-Path $rep)
Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*edge_prof*' -and $_.CommandLine -like '*web*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false -ErrorAction SilentlyContinue }
Start-Sleep 3
Remove-Item -Recurse -Force $ud -ErrorAction SilentlyContinue
