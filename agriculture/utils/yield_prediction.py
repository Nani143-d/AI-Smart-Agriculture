from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml_models" / "yield_model.pkl"

def predict_yield(data):
    if MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            # Training script documents this feature order.
            features = [[data["nitrogen"], data["phosphorus"], data["potassium"],
                         data["temperature"], data["rainfall"]]]
            value = float(model.predict(features)[0])
            return {"yield_t_ha": round(max(0, value), 2), "method": "trained ML model",
                    "notice": "Estimate only. Accuracy depends on the training data and local farming conditions."}
        except Exception:
            pass
    # Clearly labeled baseline demo, not a scientifically validated prediction.
    value = max(0.0, 1.5 + data["nitrogen"] * 0.02 + data["temperature"] * 0.03 + data["rainfall"] * 0.01)
    return {"yield_t_ha": round(value, 2), "method": "demo baseline (not a trained model)",
            "notice": "Demo estimate only—not a reliable agricultural forecast. Train and install yield_model.pkl using local crop-yield data."}
