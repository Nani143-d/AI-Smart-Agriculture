from pathlib import Path
import json
import logging

import numpy as np

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml_models" / "disease_model.keras"
LABELS_PATH = BASE_DIR / "ml_models" / "disease_labels.json"

logger = logging.getLogger(__name__)

# Cache the model and labels after loading
_model = None
CLASS_LABELS = None


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_disease_model():
    global _model, CLASS_LABELS

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Disease model not found: {MODEL_PATH}"
        )

    if not LABELS_PATH.is_file():
        raise FileNotFoundError(
            f"Disease labels not found: {LABELS_PATH}"
        )

    import tensorflow as tf

    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)

    if CLASS_LABELS is None:
        with open(LABELS_PATH, "r", encoding="utf-8") as file:
            CLASS_LABELS = json.load(file)

    if not isinstance(CLASS_LABELS, list) or not CLASS_LABELS:
        raise ValueError("The disease labels file is invalid.")

    output_shape = _model.output_shape
    if isinstance(output_shape, list):
        raise ValueError("The model has multiple outputs.")

    if output_shape[-1] != len(CLASS_LABELS):
        raise ValueError(
            f"Model outputs {output_shape[-1]} classes, "
            f"but labels contain {len(CLASS_LABELS)} classes."
        )

    return _model, CLASS_LABELS


# --------------------------------------------------
# PREDICT PLANT DISEASE
# --------------------------------------------------

def predict_disease(image_path):
    try:
        from PIL import Image

        model, labels = load_disease_model()

        # Read the uploaded image
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            image = image.resize((224, 224))

            image_array = np.asarray(
                image,
                dtype=np.float32
            )

        # IMPORTANT:
        # If your training script used rescale=1./255 or
        # a Rescaling layer, match that preprocessing here.
        image_array = image_array / 255.0

        # Add batch dimension: (1, 224, 224, 3)
        image_array = np.expand_dims(image_array, axis=0)

        # Run model prediction
        predictions = model.predict(image_array, verbose=0)
        probabilities = np.asarray(predictions).squeeze()

        if probabilities.ndim != 1:
            raise ValueError(
                f"Unexpected prediction shape: {predictions.shape}"
            )

        if len(probabilities) != len(labels):
            raise ValueError(
                "Prediction count does not match the label count."
            )

        if not np.all(np.isfinite(probabilities)):
            raise ValueError("The model returned invalid values.")

        # Get the highest-scoring class
        predicted_index = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_index]) * 100
        disease_name = labels[predicted_index].replace("__", " - ").replace("_", " ")

        return {
            "label": disease_name,
            "confidence": round(confidence, 2),
            "message": (
                f"Predicted class: {disease_name}. "
                "Please confirm the result with an agricultural expert."
            ),
        }

    except Exception as error:
        logger.exception("Plant disease prediction failed.")

        return {
            "label": "Prediction Error",
            "confidence": None,
            "message": (
                "The image could not be analyzed. "
                f"Error: {error}"
            ),
        }