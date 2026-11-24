# Live-site test in headless Edge, read back over the DevTools protocol (no files or endpoints needed on the site).
#   -Mode probe : load the page, check the YouTube player is ready, play ~8 s, seek, report state.
#   -Mode full  : run the 11-question self-test against the live narrator (costs ~11 Anthropic answers).
param([ValidateSet('probe', 'full')][string]$Mode = 'probe', [string]$Site = 'https://undergrad-recap.web.app/', [int]$TimeoutMin = 40, [string]$Yt = '')
$ErrorActionPreference = 'Stop'
$w = $PSScriptRoot
$ud = "$w\edge_live_prof"; $port = 9333
$url = $Site + '?t=0' + $(if ($Yt) { "&yt=$Yt" } else { '' })
if ($Mode -eq 'full') {
  $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$w\local\selftest_cases.json"))
  $url = $Site + '?selftest=1#cases=' + [Uri]::EscapeDataString($b64)
}
$a = @('--headless=new', '--inprivate', '--disable-sync', '--no-first-run', '--disable-extensions', '--disable-gpu',
       '--autoplay-policy=no-user-gesture-required', '--mute-audio', "--remote-debugging-port=$port",
       '--disable-background-media-suspend', '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--disable-backgrounding-occluded-windows',
       "--user-data-dir=$ud", $url)
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList $a | Out-Null

function Cleanup {
  Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*edge_live_prof*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false -ErrorAction SilentlyContinue }
  Start-Sleep 3; Remove-Item -Recurse -Force $ud -ErrorAction SilentlyContinue
}
try {
  $ws = $null
  for ($i = 0; $i -lt 40 -and -not $ws; $i++) {
    Start-Sleep -Milliseconds 500
    try { $list = Invoke-RestMethod "http://127.0.0.1:$port/json"; $ws = ($list | ForEach-Object { $_ } | Where-Object { $_.type -eq 'page' -and $_.url -like "$Site*" } | Select-Object -First 1).webSocketDebuggerUrl } catch {}
  }
  if (-not $ws) { throw 'no debuggable page' }
  $sock = New-Object System.Net.WebSockets.ClientWebSocket
  $ct = [Threading.CancellationToken]::None
  $sock.ConnectAsync([Uri]$ws, $ct).Wait()
  $script:id = 0
  function Eval([string]$expr) {
    $script:id++
    $msg = @{ id = $script:id; method = 'Runtime.evaluate'; params = @{ expression = $expr; returnByValue = $true; awaitPromise = $true } } | ConvertTo-Json -Compress -Depth 5
    $bytes = [Text.Encoding]::UTF8.GetBytes($msg)
    $sock.SendAsync((New-Object ArraySegment[byte] (, $bytes)), 'Text', $true, $ct).Wait()
    while ($true) {
      $ms = New-Object IO.MemoryStream; $buf = New-Object byte[] 65536
      do { $r = $sock.ReceiveAsync((New-Object ArraySegment[byte] (, $buf)), $ct).Result; $ms.Write($buf, 0, $r.Count) } while (-not $r.EndOfMessage)
      $o = [Text.Encoding]::UTF8.GetString($ms.ToArray()) | ConvertFrom-Json
      if ($o.id -eq $script:id) { return $o.result.result.value }
    }
  }
  $state = '(() => { const v = typeof V === "undefined" ? null : V; const p = v && v.p;
    return JSON.stringify({ ready: !!(v && v._ready), dur: v ? v.duration : null, t: v ? +v.currentTime.toFixed(2) : null, paused: v ? v.paused : null,
      ytState: p && p.getPlayerState ? p.getPlayerState() : null, err: v ? (v.error ?? null) : null, scale: SCALE, marks: !!MARKS,
      where: document.getElementById("where") ? document.getElementById("where").textContent : "", hint: document.getElementById("hint").textContent,
      quality: p && p.getPlaybackQuality ? p.getPlaybackQuality() : null, levels: p && p.getAvailableQualityLevels ? p.getAvailableQualityLevels() : null }); })()'
  $sw = [Diagnostics.Stopwatch]::StartNew()
  if ($Mode -eq 'probe') {
    while ($sw.Elapsed.TotalSeconds -lt 45) { $j = Eval $state; if (-not $j) { Start-Sleep 1; continue }; $s = $j | ConvertFrom-Json; if ($s.ready -or $null -ne $s.err) { break }; Start-Sleep 1 }
    "after {0:N1}s: {1}" -f $sw.Elapsed.TotalSeconds, (Eval $state)
    if ($s.ready) {
      Eval 'V.play().then(() => "ok")' | Out-Null; Start-Sleep 8; "playing 8s: " + (Eval $state)
      Eval '(V.currentTime = 3600, "ok")' | Out-Null; Start-Sleep 5; "seek 1:00:00: " + (Eval $state)
      Eval '(V.pause(), "ok")' | Out-Null; Start-Sleep 1; "paused: " + (Eval $state)
    }
  } else {
    $last = -1
    while ($sw.Elapsed.TotalMinutes -lt $TimeoutMin) {
      Start-Sleep 5
      $st = Eval 'JSON.stringify(window.__selftest || null)' | ConvertFrom-Json
      if ($st -and $st.results.Count -ne $last) { $last = $st.results.Count; "{0:N0}s: {1} cases done" -f $sw.Elapsed.TotalSeconds, $last }
      if ($st -and $st.done) { break }
      if (-not $st -and $sw.Elapsed.TotalSeconds -gt 60) { "no self-test after 60s: " + (Eval $state); break }
    }
    $out = "$w\live_selftest_report.json"
    if ($st) { $st | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 $out; "report -> $out" }
  }
  $sock.Dispose()
} finally { Cleanup }
