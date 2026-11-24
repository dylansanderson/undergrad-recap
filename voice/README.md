# Voice model (not committed)

Narration uses **Kokoro v1.0** (ONNX), voice **`af_heart`**, speed 1.0. Two files must be here:

| File | Size | Source |
|---|---|---|
| `kokoro-v1.0.onnx` | 325,532,387 bytes | https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx |
| `voices-v1.0.bin` | 28,214,398 bytes | https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin |

```powershell
foreach ($f in 'kokoro-v1.0.onnx','voices-v1.0.bin') { Invoke-WebRequest "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f" -OutFile $f }
```

Who loads them:

- `build/tts.py` and `local-narrator/tts.py` look in `<their folder>/voice/` first and then fall back to this folder (`../voice`).
- The Cloud Run image needs its own copy in `web/server/voice/`, because the Dockerfile does `COPY voice/ voice/`. `web/deploy_narrator.ps1` copies the files there automatically if they're missing.

Audio rules (do not change without listening first): per-sentence synthesis, trimmed, short fades, gentle compression and loudness normalisation, static gain and **no** limiter or extra compressor. That combination fixed the loud, crackly first word of each sentence.
