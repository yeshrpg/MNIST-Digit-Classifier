import numpy as np
from tensorflow import keras
from PIL import Image
import io

MODEL_PATH = "mnist_cnn.keras"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = keras.models.load_model(MODEL_PATH)
    return _model

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("L")
    img = img.resize((28, 28))
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=(0, -1))  # shape (1, 28, 28, 1)
    return arr

def predict_digit(image_bytes: bytes):
    model = get_model()
    arr = preprocess_image(image_bytes)
    preds = model.predict(arr, verbose=0)[0]
    predicted_class = int(np.argmax(preds))
    confidence = float(np.max(preds))
    return predicted_class, confidence, preds.tolist()