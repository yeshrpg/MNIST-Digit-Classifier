# CLAUDE.md — Agent Context for MNIST Digit Classifier

You are working inside a spec-driven repo. **Read PRD.md, schema.md, and architecture.md before writing any code.** These are locked decisions — do not redesign the architecture, swap the tech stack, or change the API contract mid-build. If something in tasks.md seems to conflict with the spec, stop and ask rather than improvising a fix.

## Project in one line
A canvas web app where a user draws a digit and a FastAPI-served CNN predicts it live. Two deployables: FastAPI backend (Render, Docker) + vanilla JS frontend (Vercel).

## Non-negotiable constraints
- Backend: FastAPI, not Flask/Django.
- Frontend: vanilla HTML/CSS/JS, no React/Vue — this is intentional (see architecture.md rationale table), do not suggest adding a framework.
- Model: CNN per the exact architecture in schema.md, not the original notebook's Dense NN.
- Preprocessing happens server-side (in `inference.py`), not client-side.
- Read `PORT` from environment in the backend — Render requires this, hardcoding 8000 will break deployment.
- Model artifact format: `.keras` (native), not `.h5`.

## Working order
Follow tasks.md phase by phase (Model → Backend → Frontend → Deployment → Polish). Don't jump to deployment before the local end-to-end flow works — Phase 2's T2.8 (local curl test) must pass before starting Phase 3.

## Known tricky spot
The canvas-to-model preprocessing pipeline (schema.md) has a step flagged as "critical, must be verified, not assumed": whether the canvas image needs color inversion before feeding the model (MNIST is white digit on black; canvas is typically black stroke on white). Test this explicitly with a real drawn sample — don't assume it works just because the code runs without errors.

## Style
- Keep functions small and testable — `inference.py`'s `predict()` should be a pure function callable outside of FastAPI for easy debugging.
- Comment the "why" on the inversion/normalization steps specifically, since that's the part most likely to silently produce wrong (but not erroring) predictions.

## When you're done with a phase
Update tasks.md checkboxes as you complete items. Don't mark a task done until it's actually verified (e.g. T1.2's accuracy threshold actually checked, not assumed).
