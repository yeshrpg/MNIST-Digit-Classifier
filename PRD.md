# PRD.md — MNIST Digit Classifier

## 1. Product Summary
A web app where a user draws a single handwritten digit (0–9) on a canvas and receives a live AI prediction with per-class confidence scores. Built to demonstrate an end-to-end ML product: trained model → served API → deployed public frontend.

## 2. Goals
- Showcase a real, working, deployed full-stack ML app for an internship application/resume.
- Demonstrate: model training, API design, containerized deployment, clean frontend UX.
- Keep scope tight — one feature, done well, not a feature-bloated app.

## 3. Non-Goals
- No user accounts/auth.
- No multi-digit / sequence recognition (single digit only).
- No persistent storage of user drawings (privacy-friendly, stateless).

## 4. Users & Use Case
- Primary: internship reviewer/recruiter clicking a live link, drawing a digit, seeing it work in <2 seconds.
- Secondary: YESH, demoing in an interview and explaining the architecture.

## 5. Core User Flow
1. User opens the Vercel-hosted frontend.
2. User draws a digit on an HTML canvas (mouse or touch).
3. On "Predict" (or debounced auto-predict), the canvas image is downsampled to 28x28 grayscale and POSTed to the backend `/predict` endpoint.
4. Backend returns predicted digit + confidence array for all 10 classes.
5. Frontend displays the predicted digit large, plus a small bar chart of all 10 confidences.
6. "Clear" button resets the canvas.

## 6. Functional Requirements
- FR1: Canvas supports mouse and touch drawing, adjustable brush size defaulted sensibly for digit strokes.
- FR2: Client-side preprocessing (resize to 28x28, grayscale, normalize) OR server-side — decision: **server-side**, so the model/preprocessing logic lives in one place and frontend just sends raw canvas image data (see architecture.md).
- FR3: `/predict` endpoint returns JSON: `{ "predicted_digit": int, "confidences": [float x10] }`.
- FR4: `/health` endpoint for uptime checks / Render health probe.
- FR5: Frontend shows a loading state while waiting on prediction (target latency <1s on Render free tier after cold start).
- FR6: Graceful error state if backend is unreachable or cold-starting (Render free tier sleeps after inactivity).

## 7. Model Requirements
- Upgrade from the original notebook's Dense NN to a CNN for higher accuracy (~99% target vs. notebook's 97.1%).
- Trained on standard Keras MNIST dataset (60k train / 10k test).
- Exported as a single artifact loaded once at API startup (no retraining per request).

## 8. Success Metrics
- Test accuracy ≥ 98.5%.
- Correctly classifies hand-drawn digits from the canvas (not just the original MNIST test set) — canvas-drawn digits differ in stroke width/style, so this is validated manually post-deploy.
- Public URL loads and returns a prediction end-to-end within 10s (including Render cold start).

## 9. Constraints
- Free-tier hosting only (Render + Vercel) — must design around Render free-tier cold starts and no persistent disk beyond the committed model file.
- Repo must be self-explanatory for an interviewer skimming it (clean README, clear structure).

## 10. Out of Scope for v1
- CI/CD pipeline (may be added later as a resume enhancement, not required for v1 ship).
- Automated tests beyond basic API smoke tests.
