from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import predict_digit
from schemas import PredictionResponse

app = FastAPI(title="MNIST Digit Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your Vercel domain once deployed
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    image_bytes = await file.read()
    digit, confidence, probs = predict_digit(image_bytes)
    return PredictionResponse(digit=digit, confidence=confidence, probabilities=probs)