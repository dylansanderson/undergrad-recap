# Rebuild and redeploy the Cloud Run narrator (web/server) and check it answers.
# Existing service settings (4 vCPU / 4Gi, max 1 instance, secrets, env vars) are kept by `gcloud run deploy`.
# Takes ~5-8 min (Cloud Build builds the image). The site keeps working during the deploy; the switch is instant.
$ErrorActionPreference = 'Stop'
$g = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
$srv = Join-Path $PSScriptRoot 'server'
$voice = Join-Path (Split-Path $PSScriptRoot -Parent) 'voice'
New-Item -ItemType Directory -Force "$srv\voice" | Out-Null
foreach ($f in 'kokoro-v1.0.onnx', 'voices-v1.0.bin') {
    if (-not (Test-Path "$srv\voice\$f")) {
        if (-not (Test-Path "$voice\$f")) { throw "missing $voice\$f (see voice/README.md)" }
        Copy-Item "$voice\$f" "$srv\voice\$f"
    }
}
Push-Location $srv
try { & $g run deploy narrator --source . --region=us-central1 --project=undergrad-recap --quiet; if ($LASTEXITCODE) { throw "deploy failed ($LASTEXITCODE)" } }
finally { Pop-Location }
$r = Invoke-RestMethod 'https://undergrad-recap.web.app/api/warm' -TimeoutSec 90
"warm: ok=$($r.ok) voice=$($r.voice) narrator=$($r.narrator)"
