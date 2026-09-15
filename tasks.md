# tasks.md — MNIST Digit Classifier

Spec is locked (PRD.md, schema.md, architecture.md). Do not re-decide architecture while executing these — flag back if a task reveals a spec gap instead of improvising.

## Phase 1 — Model
- [ ] T1.1: Write `train.py` — load keras MNIST dataset, build CNN per schema.md, train, evaluate on test set.
- [ ] T1.2: Confirm test accuracy ≥ 98.5% (PRD success metric). If not met, tune (more epochs / add a conv block) before moving on.
- [ ] T1.3: Save model to `backend/model/mnist_cnn.keras`.
- [ ] T1.4: Manually sanity-check the model against 2-3 real hand-drawn digit images (not the MNIST test set) to catch inversion/preprocessing issues early.

## Phase 2 — Backend
- [ ] T2.1: Scaffold FastAPI app structure per architecture.md (`main.py`, `inference.py`, `model_loader.py`, `schemas.py`).
- [ ] T2.2: Implement `model_loader.py` — load model once at startup.
- [ ] T2.3: Implement `inference.py` preprocessing pipeline per schema.md (decode base64 → grayscale → resize 28x28 → verify inversion → normalize → reshape).
- [ ] T2.4: Implement `POST /predict` and `GET /health` routes per schema.md contract.
- [ ] T2.5: Add CORS middleware reading `ALLOWED_ORIGINS` from env.
- [ ] T2.6: Read `PORT` from env (Render requirement), not hardcoded.
- [ ] T2.7: Write `Dockerfile` (python slim base, install requirements, copy app + model, run uvicorn).
- [ ] T2.8: Test locally end-to-end with `curl` or Postman against a real base64 PNG before touching the frontend.

## Phase 3 — Frontend
- [ ] T3.1: Build `index.html` with a fixed-size canvas (e.g. 280x280 for comfortable drawing, downsized server-side).
- [ ] T3.2: Implement drawing in `canvas.js` (mouse + touch events).
- [ ] T3.3: "Predict" button: export canvas to base64 PNG, POST to backend, render response.
- [ ] T3.4: "Clear" button: reset canvas.
- [ ] T3.5: Display predicted digit prominently + confidence bar chart for all 10 classes.
- [ ] T3.6: Loading state while waiting on response (esp. Render cold start — show a distinct "waking up server, first request may take ~30s" message).
- [ ] T3.7: Error state for failed/unreachable backend.

## Phase 4 — Deployment
- [ ] T4.1: Push repo to GitHub.
- [ ] T4.2: Deploy `backend/` to Render as a Docker web service; set `ALLOWED_ORIGINS` once frontend URL is known.
- [ ] T4.3: Deploy `frontend/` to Vercel (root directory = `frontend/`); set `API_BASE_URL` to the live Render URL.
- [ ] T4.4: Re-deploy backend with correct `ALLOWED_ORIGINS` once Vercel URL is confirmed (chicken-and-egg — expect one round trip here).
- [ ] T4.5: End-to-end test on the live public URLs, not just localhost.

## Phase 5 — Polish (resume-readiness)
- [ ] T5.1: Write a clear `README.md` — what it does, live demo link, architecture diagram/summary, how to run locally, tech stack list.
- [ ] T5.2: Add a short GIF/screenshot of the app working to the README.
- [ ] T5.3: Clean commit history / meaningful commit messages if this will be shown as a portfolio repo.
