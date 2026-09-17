# MNIST Digit Classifier — End-to-End Deployed ML App

A handwritten digit classifier that goes beyond a notebook demo: a CNN trained to **99.14% test accuracy**, served through a production FastAPI backend, containerized with Docker, and connected to a live canvas-based frontend — fully deployed and publicly usable.

**Live demo:** https://mnist-digit-classifier-nu.vercel.app

**API docs (Swagger):** https://mnist-digit-classifier-backend.onrender.com/docs

---

## Why this isn't "just another MNIST notebook"

Most MNIST projects stop at `model.fit()` and a confusion matrix in a Jupyter cell. This one was built as a real, shippable product:

- **Full-stack, not just a model** — a trained CNN is only useful if something can call it. This has a REST API in front of the model with request/response schema validation, and a real frontend a non-technical person can use with a mouse.
- **Draw-to-predict UX** — a canvas-based frontend where you draw a digit by hand (not upload a pre-cropped MNIST test image), which is a meaningfully harder and more realistic input than the clean 28×28 dataset images the model was trained on.
- **Containerized for portability** — the backend runs identically locally and in production via Docker, with the container correctly binding to a platform-assigned port (`$PORT`) rather than a hardcoded one, which is a detail most hobby deployments get wrong on the first try.
- **Actually deployed, not just "deploy-ready"** — backend live on Render, frontend live on Vercel, wired together and tested end-to-end in production (not just `localhost`), including catching and fixing a real CORS/endpoint-path bug during deployment rather than leaving it as a known issue.
- **Clean, professional git history** — commits follow conventional commit format (`feat:`, `fix:`, `chore:`, `docs:`) and the repo was rebased to remove noisy WIP commits, so the history reads like a maintained project, not a scratchpad.
- **Documented like a real project** — architecture, product requirements, and task breakdown were written as planning docs before/alongside the build, not reverse-engineered after the fact.

---

## Architecture

```
┌─────────────────────┐         HTTPS POST /predict           ┌──────────────────────────┐
│   Frontend (Vercel) │ ──────────────────────────────────▶  │  Backend (Render, Docker) │
│  HTML5 Canvas + JS  │                                       │  FastAPI + Pydantic      │
│  draw → base64 image│ ◀──────────────────────────────────  │  TensorFlow/Keras CNN     │
└─────────────────────┘         JSON: {digit, confidence}     └──────────────────────────┘
```

1. User draws a digit on an HTML5 `<canvas>`.
2. Frontend JS captures the canvas as image data and POSTs it to the backend.
3. FastAPI validates the request against a Pydantic schema, preprocesses the image (resize/normalize to match MNIST's 28×28 grayscale format), and runs it through the trained CNN.
4. The model returns a predicted digit and confidence score, rendered back on the page.

---

## Tech stack

| Layer | Tech |
|---|---|
| Model | TensorFlow / Keras CNN, trained on MNIST |
| Backend | FastAPI, Pydantic (schema validation), Uvicorn |
| Containerization | Docker |
| Frontend | Vanilla HTML5 Canvas + JavaScript (no framework) |
| Backend hosting | Render (Docker web service) |
| Frontend hosting | Vercel |

**Model performance:** 99.14% test accuracy on the MNIST test set.

---

## Local setup

**Backend:**
```bash
git clone https://github.com/yeshrpg/MNIST-Digit-Classifier.git
cd MNIST-Digit-Classifier/backend
pip install -r requirements.txt
uvicorn main:app --reload
```
API available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

**Or run the backend in Docker (matches production exactly):**
```bash
cd backend
docker build -t mnist-backend .
docker run -p 8000:8000 mnist-backend
```

**Frontend:**
Open `frontend/index.html` directly in a browser, or serve it with any static server. Update the API URL in `script.js` to point to your local backend if testing locally.

---

## Project structure

```
MNIST-Digit-Classifier/
├── backend/
│   ├── main.py              # FastAPI app + /predict endpoint
│   ├── model/                # trained CNN weights
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html            # canvas UI
│   └── script.js             # draw capture + API call
├── docs/
│   ├── architecture.md
│   ├── PRD.md
│   ├── schema.md
│   └── tasks.md
└── README.md
```

---

## Docs

Full planning documentation is in `/docs`:
- `architecture.md` — system design decisions
- `PRD.md` — product requirements
- `schema.md` — API request/response schema
- `tasks.md` — build task breakdown

---

## Author

Built by [yeshrpg](https://github.com/yeshrpg) as an internship-ready, production-style ML deployment project.
