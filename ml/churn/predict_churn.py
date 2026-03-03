import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "volunteer_churn_rf_model.pkl")
model = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    "completed_tasks",
    "trust_score",
    "avg_session_hours",
    "missed_sessions",
    "days_active"
]

def predict_churn(volunteer: dict) -> float:
    features = [[
        volunteer.get("completed_tasks", 0),
        volunteer.get("trust_score", 0),
        volunteer.get("avg_session_hours", 1.5),
        volunteer.get("missed_sessions", 0),
        volunteer.get("days_active", 30)
    ]]

    churn_probability = model.predict_proba(features)[0][1]
    return round(float(churn_probability), 3)
