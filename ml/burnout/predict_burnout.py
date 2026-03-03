import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "volunteer_burnout_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_burnout(volunteer: dict) -> float:
    """
    Returns burnout score (0–1)
    """

    features = np.array([[
        volunteer["weekly_hours"],
        volunteer["night_shifts"],
        volunteer["elder_count"],
        volunteer["stress_reports"]
    ]])

    burnout_score = model.predict(features)[0]
    return round(float(burnout_score), 3)
