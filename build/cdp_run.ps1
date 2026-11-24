param([string]$Url, [string]$StepsFile, [int]$W = 1600, [int]$H = 1000)
# Headless Edge (InPrivate, no sync/extensions, throwaway profile) driven over DevTools: runs steps from a JSON file.
# step = {"m": "<CDP method>", "p": {...}, "sleep": seconds, "shot": "<png path>", "label": "..."}
$ud = Join-Path $env:TEMP "undergrad-recap-edge_cdp"
$port = 9337
$p = Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -PassThru -ArgumentList @('--headless=new', '--inprivate', '--disable-sync', '--disable-extensions', '--no-first-run', '--mute-audio', '--autoplay-policy=no-user-gesture-required', "--window-size=$W,$H", "--user-data-dir=$ud", "--remote-debugging-port=$port", $Url)
try {
  $tgt = $null
  for ($i = 0; $i -lt 40 -and -not $tgt; $i++) { Start-Sleep -Milliseconds 500; try { $tgt = (Invoke-RestMethod "http://127.0.0.1:$port/json") | Where-Object { $_.type -eq 'page' } | Select-Object -First 1 } catch {} }
  if (-not $tgt) { throw 'no devtools target' }
  $ws = New-Object System.Net.WebSockets.ClientWebSocket
  $ws.ConnectAsync([Uri]$tgt.webSocketDebuggerUrl, [Threading.CancellationToken]::None).Wait()
  $script:id = 0; $buf = New-Object byte[] (32MB)
  function Send-Cdp($method, $params) {
    $script:id++; $msg = @{ id = $script:id; method = $method; params = $params } | ConvertTo-Json -Depth 8 -Compress
    $b = [Text.Encoding]::UTF8.GetBytes($msg)
    $ws.SendAsync([ArraySegment[byte]]::new($b), 'Text', $true, [Threading.CancellationToken]::None).Wait()
    while ($true) {
      $ms = New-Object IO.MemoryStream
      do { $r = $ws.ReceiveAsync([ArraySegment[byte]]::new($buf), [Threading.CancellationToken]::None).Result; $ms.Write($buf, 0, $r.Count) } until ($r.EndOfMessage)
      $o = [Text.Encoding]::UTF8.GetString($ms.ToArray()) | ConvertFrom-Json
      if ($o.id -eq $script:id) { return $o }
    }
  }
  $steps = Get-Content $StepsFile -Raw -Encoding UTF8 | ConvertFrom-Json
  foreach ($s in $steps) {
    if ($s.sleep) { Start-Sleep -Milliseconds ([int]($s.sleep * 1000)) }
    if ($s.m) {
      $params = @{}; if ($s.p) { $s.p.PSObject.Properties | ForEach-Object { $params[$_.Name] = $_.Value } }
      $r = Send-Cdp $s.m $params
      if ($s.label) { "{0}: {1}" -f $s.label, ($(if ($r.result.result) { $r.result.result.value } else { $r.error.message })) }
    }
    if ($s.shot) { $o = Send-Cdp 'Page.captureScreenshot' @{ format = 'png' }; [IO.File]::WriteAllBytes($s.shot, [Convert]::FromBase64String($o.result.data)); "shot $($s.shot)" }
  }
} finally {
  Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
  Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*edge_cdp*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
  Start-Sleep 2; Remove-Item -Recurse -Force $ud -ErrorAction SilentlyContinue
}
