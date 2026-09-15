# schema.md — MNIST Digit Classifier

## API Contract

### `POST /predict`
**Request** (JSON):
```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```
- `image`: base64-encoded PNG/JPEG data URI of the raw canvas drawing (any resolution — backend handles resize).

**Response** (200 OK):
```json
{
  "predicted_digit": 7,
  "confidences": [0.001, 0.002, 0.01, 0.003, 0.02, 0.005, 0.001, 0.94, 0.01, 0.007]
}
```
- `predicted_digit`: int, 0–9.
- `confidences`: array of 10 floats (softmax output), index = digit, sums to ~1.0.

**Error response** (422/500):
```json
{ "error": "description of what went wrong" }
```

### `GET /health`
**Response** (200 OK):
```json
{ "status": "ok", "model_loaded": true }
```

## Internal Data Shapes

### Preprocessing pipeline (server-side, in `inference.py`)
1. Decode base64 → raw image bytes.
2. Load via PIL, convert to grayscale (`L` mode).
3. Resize to 28x28 (`Image.resize`, `LANCZOS` or `NEAREST` — test both, canvas strokes are thick so NEAREST may preserve stroke shape better).
4. Invert if needed — canvas is typically black-on-white; MNIST is white-digit-on-black. **This inversion step is critical and must be verified against a real canvas sample, not assumed.**
5. Normalize pixel values to [0,1] (divide by 255).
6. Reshape to model's expected input shape: `(1, 28, 28, 1)` for CNN.

### Model artifact
- Format: Keras `.keras` (native format, not legacy `.h5`) saved via `model.save('model/mnist_cnn.keras')`.
- Loaded once at FastAPI startup into a module-level global, reused across requests (no reload per call).

### Model architecture (CNN, replacing notebook's Dense NN)
```
Input (28,28,1)
→ Conv2D(32, 3x3, relu) → MaxPooling2D(2x2)
→ Conv2D(64, 3x3, relu) → MaxPooling2D(2x2)
→ Flatten
→ Dense(64, relu) → Dropout(0.3)
→ Dense(10, softmax)
```
Optimizer: adam. Loss: sparse_categorical_crossentropy. Metrics: accuracy.

## Environment Variables
| Var | Used by | Purpose |
|---|---|---|
| `MODEL_PATH` | backend | Path to the `.keras` model file (default: `model/mnist_cnn.keras`) |
| `ALLOWED_ORIGINS` | backend | CORS whitelist — must include the deployed Vercel frontend URL |
| `API_BASE_URL` | frontend | Backend's Render URL, injected at build/deploy time |
