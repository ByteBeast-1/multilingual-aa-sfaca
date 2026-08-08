---
title: SFA-CA Multilingual AI Attribution API
emoji: 🌐
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
short_description: Script-Family-Aware Contrastive Adaptation API (FastAPI)
---

# SFA-CA Backend API

FastAPI backend for the **Script-Family-Aware Contrastive Adaptation (SFA-CA)** multilingual AI text attribution system.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info & class list |
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze text attribution |

## Usage

```bash
curl -X POST "https://sandeepsakthi-sfaca-api.hf.space/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here..."}'
```
