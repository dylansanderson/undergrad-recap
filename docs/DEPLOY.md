# Deploying the website and narrator

All commands are run from `web/` in PowerShell. `gcloud` is not on PATH, so the scripts call it by its full path. Log in once with:

```powershell
& "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" auth login
```

## What lives where

| Change | Files | Deploy with |
|---|---|---|
| Page layout, player, styling | `web/public/index.html`, `web/public/player.js` | `deploy_hosting.py` |
| Chapters, slide list, YouTube id | `web/site_config.json`, `web/server/timeline.json` -> `build_site.py` -> `web/public/meta.json` | `build_site.py`, then `deploy_hosting.py` |
| Narrator prompt, limits, model, TTS | `web/server/app.py`, `web/server/tts.py` | `deploy_narrator.ps1` |
| Narrator settings with no code change (limits, model, on/off) | Cloud Run env vars | `gcloud run services update` (see OPERATIONS.md) |

## Website: preview first, then live

```powershell
python -P -E build_site.py            # only if timeline.json or site_config.json changed (also copies slide PDFs from Coursework)
python -P -E deploy_hosting.py preview
```

`preview` publishes to **https://undergrad-recap--preview-b5j4y7pm.web.app**. It uses the same live narrator, the live site is untouched, and the channel expires 7 days after the last preview deploy. Check it on a phone and on desktop, then:

```powershell
python -P -E deploy_hosting.py        # live, no downtime
```

To check the result:

```powershell
.\live_test.ps1                       # probe: page loads, YouTube player ready, plays, seeks (free)
.\shots.ps1                           # phone / landscape / desktop screenshots -> web\shots\
.\live_test.ps1 -Mode full            # 11 real narrator questions (costs ~11 Claude answers, a few cents)
```

## Narrator (Cloud Run)

```powershell
.\deploy_narrator.ps1
```

This takes 5–8 minutes while Cloud Build builds the image. The old revision keeps serving until the new one is ready, and the service settings (CPU, memory, secrets, env vars) are kept. It copies the voice model into `server/voice/` if needed and finishes by calling `/api/warm`.

## Rolling back

- **Website:** Firebase console -> Hosting -> Release history -> the release you want -> **Roll back**.
- **Narrator:** Cloud Run console -> `narrator` -> Revisions -> send 100 % of traffic to the previous revision.

## Taking things offline

| Goal | Command | Undo |
|---|---|---|
| Whole site offline (visitors see "Site Not Found") | `python -P -E deploy_hosting.py disable` | `python -P -E deploy_hosting.py` |
| Narrator only (video still works) | `gcloud run services update narrator --region us-central1 --project undergrad-recap --update-env-vars NARRATOR_DISABLED=1` | Same command with `NARRATOR_DISABLED=0` |

The Firebase console has **no** "disable site" button. The `disable` mode above is the equivalent of `firebase hosting:disable`.

## Local development (no cloud)

Run the web player against a local server:

```powershell
cd web
python -P -E server\app.py --static public --localdir local --video "C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Undergrad_Recap_Lectures.mp4" --selftest --port 8790
# open http://127.0.0.1:8790/?local=1 ; automated run: .\run_selftest.ps1
```

This needs `ANTHROPIC_API_KEY` set in the shell; it never goes in a file in this repo. To put a new key in the cloud, copy it to the clipboard and run `.\store_key.ps1`. The script stores the key in Secret Manager, never prints it, and clears the clipboard. Cloud Run picks the new key up on the next deploy or revision.

## The YouTube video

The id is in `web/site_config.json`. If the video is re-uploaded:

1. Set the new id in `site_config.json`.
2. Run `build_site.py`, then `deploy_hosting.py preview`, check it, then `deploy_hosting.py`.

Upload the matching `Undergrad_Recap_Lectures.srt` as subtitles, and paste `Undergrad_Recap_Lectures_YouTube_Chapters.txt` into the description. Set the video to Unlisted and turn on "Allow embedding".
