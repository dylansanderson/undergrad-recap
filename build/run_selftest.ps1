param([int]$Port = 8765)
$app = "C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator"
$ud = "$env:TEMP\undergrad-recap-edge_prof2"
Remove-Item "$app\selftest_report.json" -ErrorAction SilentlyContinue
$args = @('--headless=new', '--inprivate', '--disable-sync', '--no-first-run', '--disable-extensions', '--disable-gpu',
          '--autoplay-policy=no-user-gesture-required', '--mute-audio',
          '--disable-background-media-suspend', '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--disable-backgrounding-occluded-windows',
          "--user-data-dir=$ud", '--remote-debugging-port=9334', "http://127.0.0.1:$Port/?selftest=1")
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList $args | Out-Null
$sw = [Diagnostics.Stopwatch]::StartNew()
while (-not (Test-Path "$app\selftest_report.json") -and $sw.Elapsed.TotalMinutes -lt 40) { Start-Sleep 5 }
"elapsed {0:N0}s report={1}" -f $sw.Elapsed.TotalSeconds, (Test-Path "$app\selftest_report.json")
Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*edge_prof2*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false -ErrorAction SilentlyContinue }
Start-Sleep 3
Remove-Item -Recurse -Force $ud -ErrorAction SilentlyContinue
