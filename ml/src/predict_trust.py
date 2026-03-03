import numpy as np
import joblib
from features import FEATURES
model_path="../models/trust_model_v1.pkl"
model=joblib.load(model_path)

input_data = {
    "completed_tasks": 80,
    "cancelled_tasks": 2,
    "avg_response_time": 4.5,
    "complaints_count": 1,
    "otp_failures": 0,
    "sos_triggers": 0,
    "background_verified": 1,
    "tenure_days": 365
}

def predict_trust_score(feature_dict):
    feature_vector = [feature_dict[f] for f in FEATURES]
    score = model.predict([feature_vector])[0]
    return round(float(score), 2)
print(predict_trust_score(input_data))