# Stores the Anthropic API key from the clipboard in Google Secret Manager (project undergrad-recap).
# The key is never printed. Copy the key first, then run this script.
$g = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
$k = (Get-Clipboard -Raw)
if ($null -eq $k) { Write-Host 'Clipboard is empty. Copy the API key first.'; exit 1 }
$k = $k.Trim()
if ($k -notmatch '^sk-ant-[A-Za-z0-9_\-]{20,}$') { Write-Host 'The clipboard does not hold an Anthropic API key (it should start with sk-ant-). Nothing was stored.'; exit 1 }
$tmp = [IO.Path]::GetTempFileName()
try {
    [IO.File]::WriteAllText($tmp, $k, (New-Object Text.UTF8Encoding $false))
    & $g secrets describe anthropic-api-key --project=undergrad-recap *> $null
    if ($LASTEXITCODE -eq 0) { & $g secrets versions add anthropic-api-key --data-file=$tmp --project=undergrad-recap }
    else { & $g secrets create anthropic-api-key --replication-policy=automatic --data-file=$tmp --project=undergrad-recap }
    if ($LASTEXITCODE -eq 0) { Write-Host "Stored. Key ending ...$($k.Substring($k.Length - 4)) is now in Secret Manager as 'anthropic-api-key'." }
} finally {
    Remove-Item $tmp -Force
    Set-Clipboard -Value ' '
    Write-Host 'Clipboard cleared.'
}
