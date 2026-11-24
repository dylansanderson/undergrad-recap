# Architecture

```
                 visitor's browser
                        |
        https://undergrad-recap.web.app   (Firebase Hosting, CDN)
          |                         |
  static files                  /api/**  (rewrite)
  index.html, player.js,            |
  meta.json, slides/*.pdf           v
          |              Cloud Run service "narrator" (us-central1)
          |                 app.py + Kokoro TTS + timeline.json
  YouTube embed             |            |              |
  (video nkAxsz9Yh4Q)   Anthropic API  Secret Manager  gs://undergrad-recap-state
                        (Claude)       (API key,       (daily/monthly counters,
                                        budget token)   budget-off flag)

  Billing budget $10/mo --> Pub/Sub topic budget-alerts --> push --> /api/budget --> narrator turns itself off for the month
```

## Who does what

| Piece | Service | Role |
|---|---|---|
| Video | **YouTube** (unlisted) | Streams the 9-hour video. The page embeds it with the IFrame API and reads the current time. |
| Website | **Firebase Hosting** (site `undergrad-recap`) | Serves `web/public/` from a CDN with free SSL. It also rewrites `/api/**` to Cloud Run, so the site and API share one origin (no CORS). |
| Narrator API | **Cloud Run** `narrator` | 4 vCPU, 4 GiB, min 0 / max 1 instance, billed per request. It scales to zero when nobody is asking, so cold starts take a few seconds. |
| Claude | **Anthropic API** | `claude-opus-5-5`, effort low, streaming. Each finished sentence is voiced while the rest is still being written. |
| Secrets | **Secret Manager** | `anthropic-api-key` and `budget-token`, both mounted as env vars on Cloud Run |
| State | **Cloud Storage** `gs://undergrad-recap-state/state.json` | Per-day and global question counts, plus the "over budget this month" flag |
| Kill switch | **Billing budget, Pub/Sub** | When the budget sends an alert at 100 %, the narrator disables itself until next month. Alerts at 50 % and 90 % are informational. |
| Container images | **Artifact Registry** `cloud-run-source-deploy` | Created automatically by `gcloud run deploy --source` |

Firebase is a layer on top of the same Google Cloud project, also called `undergrad-recap`. The Firebase console only shows Hosting, while everything else (Cloud Run, secrets, billing, storage) appears in the Google Cloud console.

## How a question flows

1. The visitor pauses and asks. `player.js` POSTs `{t: series time, question, history}` to `/api/ask`.
2. `app.py` looks up `t` in `timeline.json` to find the lecture, slide, beat, bullets, code, and what the narrator just said. It builds the prompt and starts a streaming Claude call in a background job.
3. The browser long-polls `/api/job/<id>`, which keeps Cloud Run's CPU allocated. Each completed sentence is synthesized with Kokoro and served as `/api/clip/<id>/<n>.mp3`. Code blocks and whiteboard SVGs come back as text and are drawn on the page, not spoken.
4. The limits are 15 questions per visitor per hour, 50 per visitor per day and 400 per day for the whole site. They are set with the env vars `LIMIT_PER_IP_HOUR`, `LIMIT_PER_IP_DAY` and `LIMIT_GLOBAL_DAY`.

## `timeline.json`: the contract between the build and the narrator

`build/build2.py` writes `out/Undergrad_Recap_Lectures_timeline.json`. It maps every second of the combined video to its lesson, slide and beat, and records each slide's text, code and narration. Three things depend on it matching the uploaded video exactly:

- `web/server/timeline.json`, which the Cloud Run narrator uses for context
- `web/public/meta.json`, which `web/build_site.py` generates from it to build the chapter and slide navigation
- `local-narrator/timeline.json`, which the offline player uses

**Whenever the video is rebuilt, all three must be updated together, and the new video must be re-uploaded to YouTube.** See BUILD_VIDEOS.md.

## Local vs web narrator

| | `local-narrator/` | `web/` |
|---|---|---|
| Video | local MP4 | YouTube |
| Claude | `claude -p` CLI (your Claude login, no key) | Anthropic API (API key, billed) |
| Runs | `Watch with Ask-the-Narrator.bat` in Coursework | Cloud Run |
