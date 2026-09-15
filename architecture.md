# architecture.md — MNIST Digit Classifier

## System Overview
```
[Browser: Canvas UI]  --POST /predict-->  [FastAPI on Render]  --loads once-->  [mnist_cnn.keras]
      ^                                          |
      |__________ JSON response ________________|

Frontend static files served from Vercel.
```

Two independently deployable services, one repo (monorepo with `backend/` and `frontend/` folders — NOT two separate repos within this project; "2 separate repos" from your instruction refers to MNIST vs. Breast Cancer NN being separate top-level repos, not backend/frontend within MNIST).

## Repo Structure
```
mnist-digit-classifier/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, route definitions, CORS setup
│   │   ├── inference.py     # preprocessing + model.predict() wrapper
│   │   ├── model_loader.py  # loads .keras model once at startup
│   │   └── schemas.py       # Pydantic request/response models
│   ├── model/
│   │   └── mnist_cnn.keras  # trained model artifact (committed to repo)
│   ├── train.py             # standalone training script (run once, produces the .keras file)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── index.html
│   ├── canvas.js            # drawing logic + fetch() call to backend
│   ├── style.css
│   └── vercel.json           # optional Vercel config (env var injection)
├── PRD.md
├── schema.md
├── architecture.md
├── tasks.md
├── CLAUDE.md
└── README.md
```

## Component Responsibilities
- **`train.py`**: run locally/in Colab once. Loads keras MNIST dataset, builds the CNN (schema.md), trains, evaluates, saves to `backend/model/mnist_cnn.keras`. Not run in production — it's a one-time artifact generator.
- **`model_loader.py`**: loads the `.keras` file into memory at FastAPI startup (via a `lifespan` context or `@app.on_event("startup")`), stored as a module-level singleton. Avoids reloading the model on every request.
- **`inference.py`**: pure function `predict(image_base64: str) -> dict` — does preprocessing (schema.md pipeline) + `model.predict()` + formats the response. Kept separate from `main.py` so it's independently testable.
- **`main.py`**: thin FastAPI layer — route handlers call into `inference.py`, handle errors, set CORS headers from `ALLOWED_ORIGINS`.
- **`canvas.js`**: drawing state machine (mousedown/mousemove/touchmove → draw), "Predict" and "Clear" buttons, canvas→base64 export, fetch to backend, renders response as digit + confidence bars.

## Deployment Architecture
- **Backend → Render**: Dockerized web service. Render builds from the `Dockerfile` in `backend/`, exposes port via `$PORT` env var (Render injects this — `main.py` must read `PORT` from env, not hardcode 8000).
- **Frontend → Vercel**: static site deploy, root directory set to `frontend/`. `API_BASE_URL` set as a Vercel environment variable, read by `canvas.js` at runtime (or baked in at a simple build step — no framework needed, so likely a small `config.js` generated from the env var, or just hardcoded post-deploy since this is a 2-file frontend).
- **CORS**: backend's `ALLOWED_ORIGINS` must explicitly list the Vercel production URL (and `localhost` for local dev).
- **Cold starts**: Render free tier sleeps after ~15 min inactivity; first request after sleep can take 30-50s. Frontend must show a "waking up the model server..." loading state rather than failing silently (see PRD FR6).

## Local Development
- Backend: `uvicorn app.main:app --reload` from `backend/`, requires `model/mnist_cnn.keras` to already exist (run `train.py` first).
- Frontend: open `index.html` directly or serve via any static server; point `API_BASE_URL` at `http://localhost:8000`.

## Key Architectural Decisions & Rationale
| Decision | Alternative considered | Why this choice |
|---|---|---|
| FastAPI over Flask | Flask | Async support, auto OpenAPI docs (`/docs`), stronger resume signal |
| Server-side preprocessing | Client-side (JS) resize/normalize | Keeps all ML logic in one language/place, easier to test and reason about, avoids duplicating preprocessing logic if frontend changes |
| Vanilla JS frontend | React | One canvas + one fetch call doesn't justify a framework; leaner repo, faster to explain in an interview |
| CNN over Dense NN | Keep notebook's Dense NN | Meaningfully higher accuracy (~99% vs 97.1%) for similar complexity; shows deliberate model-improvement decision-making |
| Render + Vercel (split) | Both on Render / both on Vercel | Vercel doesn't run long-lived Python processes well; Render doesn't need to host a trivial static frontend — using each for its strength |
