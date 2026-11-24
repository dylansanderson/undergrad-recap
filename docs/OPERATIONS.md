# Operations: costs, limits, links

## Monthly cost (typical)

| Item | Cost |
|---|---|
| Firebase Hosting | Free (Spark-level usage: 10 GB storage, 360 MB/day transfer). The PDFs are the only large downloads. |
| Cloud Run | Pennies at hobby traffic. It scales to zero and bills only while answering. |
| Anthropic API | The main variable cost (Opus, effort low, up to 6000 output tokens per answer). The real per-answer figure is in the Anthropic usage console. |
| Artifact Registry | About $0.30/month for the stored container images. It grows by about 1.2 GB per narrator deploy, so delete old images now and then. |
| Cloud Storage, Secret Manager, Pub/Sub | Effectively $0 |

A **budget of $10/month** sends alerts at 50 %, 90 % and 100 %. At 100 % Pub/Sub calls `/api/budget`, and the narrator switches itself off until the 1st of next month. The video and the site keep working. The Anthropic console has its own spend limit as a second guard.

## Narrator settings (Cloud Run env vars)

| Var | Default | Meaning |
|---|---|---|
| `NARRATOR_DISABLED` | unset | `1` turns the narrator off |
| `NARRATOR_MODEL` | `claude-opus-5-5` | Claude model |
| `LIMIT_PER_IP_HOUR` / `LIMIT_PER_IP_DAY` / `LIMIT_GLOBAL_DAY` | 15 / 50 / 400 | Question limits |
| `STATE_BUCKET` | `undergrad-recap-state` | Where counters and the budget flag are stored |
| `TTS_THREADS`, `OMP_NUM_THREADS` | 4 | Kokoro CPU threads |

To change a setting without redeploying:

```powershell
& "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" run services update narrator --region us-central1 --project undergrad-recap --update-env-vars LIMIT_GLOBAL_DAY=200
```

## Inspecting what's deployed

- `python -P -E web\list_hosting.py` prints the last five Hosting releases and every file in the live one. The Firebase console has no file browser; the files are also simply at `https://undergrad-recap.web.app/<path>`.
- Narrator logs: Cloud Run -> `narrator` -> Logs.

## Console links

| What | Link |
|---|---|
| Firebase Hosting (releases, rollback, domains) | https://console.firebase.google.com/project/undergrad-recap/hosting/sites |
| Cloud Run narrator (revisions, logs, settings) | https://console.cloud.google.com/run/detail/us-central1/narrator?project=undergrad-recap |
| Billing reports | https://console.cloud.google.com/billing/017EE7-AF6513-D4A1BA/reports |
| Budgets | https://console.cloud.google.com/billing/017EE7-AF6513-D4A1BA/budgets |
| Secret Manager | https://console.cloud.google.com/security/secret-manager?project=undergrad-recap |
| State bucket | https://console.cloud.google.com/storage/browser/undergrad-recap-state?project=undergrad-recap |
| Artifact Registry | https://console.cloud.google.com/artifacts?project=undergrad-recap |
| Anthropic usage and limits | https://console.anthropic.com/settings/limits |
| YouTube Studio | https://studio.youtube.com |
