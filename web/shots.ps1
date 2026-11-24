# Layout screenshots of a deployed site in headless Edge with device emulation (DevTools protocol).
param([string]$Site = 'https://undergrad-recap.web.app/', [string]$Out = '')
$ErrorActionPreference = 'Stop'
$w = $PSScriptRoot
if (-not $Out) { $Out = "$w\shots" }; New-Item -ItemType Directory -Force $Out | Out-Null
$ud = "$w\edge_shot_prof"; $port = 9334
$a = @('--headless=new', '--inprivate', '--disable-sync', '--no-first-run', '--disable-extensions', '--hide-scrollbars', '--mute-audio',
       '--autoplay-policy=no-user-gesture-required', "--remote-debugging-port=$port", "--user-data-dir=$ud", 'about:blank')
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList $a | Out-Null
$script:errors = @()
try {
  $ws = $null
  for ($i = 0; $i -lt 40 -and -not $ws; $i++) { Start-Sleep -Milliseconds 500
    try { $list = Invoke-RestMethod "http://127.0.0.1:$port/json"; $ws = ($list | ForEach-Object { $_ } | Where-Object { $_.type -eq 'page' } | Select-Object -First 1).webSocketDebuggerUrl } catch {} }
  $sock = New-Object System.Net.WebSockets.ClientWebSocket; $ct = [Threading.CancellationToken]::None
  $sock.ConnectAsync([Uri]$ws, $ct).Wait(); $script:id = 0
  function Send([string]$method, $params = @{}) {
    $script:id++; $msg = @{ id = $script:id; method = $method; params = $params } | ConvertTo-Json -Compress -Depth 8
    $bytes = [Text.Encoding]::UTF8.GetBytes($msg); $sock.SendAsync((New-Object ArraySegment[byte] (, $bytes)), 'Text', $true, $ct).Wait()
    while ($true) {
      $ms = New-Object IO.MemoryStream; $buf = New-Object byte[] 1048576
      do { $r = $sock.ReceiveAsync((New-Object ArraySegment[byte] (, $buf)), $ct).Result; $ms.Write($buf, 0, $r.Count) } while (-not $r.EndOfMessage)
      $o = [Text.Encoding]::UTF8.GetString($ms.ToArray()) | ConvertFrom-Json
      if ($o.method -eq 'Runtime.exceptionThrown') { $script:errors += $o.params.exceptionDetails.exception.description }
      if ($o.method -eq 'Runtime.consoleAPICalled' -and $o.params.type -eq 'error') { $script:errors += ($o.params.args | ForEach-Object { $_.value }) -join ' ' }
      if ($o.id -eq $script:id) { if ($o.error) { throw "$method : $($o.error.message)" }; return $o.result }
    }
  }
  function Js([string]$e) { (Send 'Runtime.evaluate' @{ expression = $e; returnByValue = $true; awaitPromise = $true }).result.value }
  function Shot([string]$name, [bool]$full = $false) {
    $p = @{ format = 'png' }; if ($full) { $p.captureBeyondViewport = $true
      $h = Js 'Math.ceil(document.documentElement.scrollHeight)'; $wd = Js 'document.documentElement.clientWidth'
      $p.clip = @{ x = 0; y = 0; width = $wd; height = $h; scale = 1 } }
    $d = (Send 'Page.captureScreenshot' $p).data; [IO.File]::WriteAllBytes("$Out\$name.png", [Convert]::FromBase64String($d)); "  shot $name"
  }
  function Device($wd, $ht, $mobile) {
    Send 'Emulation.setDeviceMetricsOverride' @{ width = $wd; height = $ht; deviceScaleFactor = $(if ($mobile) { 2 } else { 1 }); mobile = $mobile } | Out-Null
    Send 'Emulation.setTouchEmulationEnabled' @{ enabled = $mobile; maxTouchPoints = $(if ($mobile) { 5 } else { 1 }) } | Out-Null
    Send 'Emulation.setEmulatedMedia' @{ features = @(@{ name = 'pointer'; value = $(if ($mobile) { 'coarse' } else { 'fine' }) }, @{ name = 'hover'; value = $(if ($mobile) { 'none' } else { 'hover' }) }) } | Out-Null
  }
  function Load($url) { Send 'Page.navigate' @{ url = $url } | Out-Null
    for ($i = 0; $i -lt 60; $i++) { Start-Sleep 1; if (Js 'typeof MARKS !== "undefined" && !!MARKS && !!document.querySelector("#lecChips .chip.on")') { break } }
    Start-Sleep 2 }
  Send 'Runtime.enable' | Out-Null; Send 'Page.enable' | Out-Null

  "iPhone portrait"
  Device 390 844 $true; Load ($Site + '?t=2:10:00&nofs=1')
  Shot 'phone_portrait'
  "  state: " + (Js 'JSON.stringify({ fsBtn: $("fsBtn").textContent, lecOn: $("lecChips").querySelector(".on").textContent, lecScroll: $("lecChips").scrollLeft, chipsCentred: ["lecChips","slideChips"].map(id => { const b = $(id).getBoundingClientRect(), c = $(id).querySelector(".on").getBoundingClientRect(); return Math.round((c.left + c.width / 2) - (b.left + b.width / 2)); }), slideOn: ($("slideChips").querySelector(".on")||{}).textContent, overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth, ytFs: $("screen").src && /fs=1/.test($("screen").src) })')
  Shot 'phone_portrait_full' $true     # (a full-page capture resizes the window, so measure before it)
  Js '$("fsBtn").click(), "ok"' | Out-Null; Start-Sleep 1
  Shot 'phone_portrait_pseudofs'
  "  pseudofs: " + (Js 'JSON.stringify({ on: document.body.classList.contains("pseudofs"), label: $("fsBtn").textContent, screenH: $("screen").getBoundingClientRect().height, winH: innerHeight })')
  Js 'showBoard("Here:\n```cpp\nint main() {\n  return 0;\n}\n```", true), "ok"' | Out-Null; Start-Sleep 1; Shot 'phone_portrait_pseudofs_board'
  Js 'hideBoard(), $("fsOver").click(), "ok"' | Out-Null; Start-Sleep 1
  "  after exit: " + (Js 'JSON.stringify({ on: document.body.classList.contains("pseudofs"), label: $("fsBtn").textContent })')

  "iPhone landscape"
  Device 844 390 $true; Load ($Site + '?t=2:10:00&nofs=1')
  Shot 'phone_landscape'; Js '$("fsBtn").click(), "ok"' | Out-Null; Start-Sleep 1; Shot 'phone_landscape_pseudofs'
  Js 'exitFull(), "ok"' | Out-Null

  "Desktop"
  Device 1440 900 $false; Load ($Site + '?t=2:10:00')
  Shot 'desktop'
  "  state: " + (Js 'JSON.stringify({ nativeFS: NATIVE_FS, lecOn: $("lecChips").querySelector(".on").textContent, slideCount: $("slideChips").children.length, overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth })')
  Device 1024 768 $false; Load ($Site + '?t=6:30:00'); Shot 'laptop_small'
  "errors: " + ($(if ($script:errors.Count) { $script:errors -join ' | ' } else { 'none' }))
  $sock.Dispose()
} finally {
  Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*edge_shot_prof*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false -ErrorAction SilentlyContinue }
  Start-Sleep 3; Remove-Item -Recurse -Force $ud -ErrorAction SilentlyContinue
}
