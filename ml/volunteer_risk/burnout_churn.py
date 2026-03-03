import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)

churn_model = joblib.load(
    os.path.join(BASE_DIR, "../churn/volunteer_churn_rf_model.pkl")
)

burnout_model = joblib.load(
    os.path.join(BASE_DIR, "../burnout/volunteer_burnout_model.pkl")
)
def predict_combined_risk(volunteer_features):
    churn_input = np.array([[
        volunteer_features["completed_tasks"],
        volunteer_features["days_since_last_task"],
        volunteer_features["avg_rating"],
        volunteer_features["trust_score"],
        volunteer_features["cancellations"],
        volunteer_features["active_days"]
    ]])

    burnout_input = np.array([[
        volunteer_features["weekly_hours"],
        volunteer_features["consecutive_days"],
        volunteer_features["night_shifts"],
        volunteer_features["emergency_tasks"],
        volunteer_features["rest_days"]
    ]])

    
    churn_probability = churn_model.predict_proba(churn_input)[0][1]
    burnout_score = burnout_model.predict(burnout_input)[0]
    if burnout_score >= 0.7 or churn_probability >= 0.7:
        decision = "BLOCK_ASSIGNMENT"
    elif burnout_score >= 0.4 or churn_probability >= 0.4:
        decision = "LIMIT_ASSIGNMENT"
    else:
        decision = "ALLOW_ASSIGNMENT"

    return {
        "churn_probability": round(float(churn_probability), 2),
        "burnout_score": round(float(burnout_score), 2),
        "decision": decision
    }
