import sys
import os
import warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pandas as pd
from ml.volunteer_risk.burnout_churn import predict_combined_risk
from ml.elders_risk.predict_risk import risk_predict
from predict_trust import predict_trust_score, input_data

def normalize(value, min_val, max_val):
    if max_val == min_val: 
        return 0.0
    value = max(min_val, min(value, max_val))
    return (value - min_val) / (max_val - min_val)

MATCHING_WEIGHTS = {
    "trust_score": 0.4,    
    "distance": 0.2,       
    "availability": 0.2,   
    "experience": 0.2       
}

def calculate_match_score(volunteer, elder_request):
    risk = predict_combined_risk(volunteer)
    churn_prob = risk["churn_probability"]
    burnout_score = risk["burnout_score"]
    availability_score = 1.0 if volunteer.get("availability", "available") == "available" else 0.5
    rating_score = volunteer.get("avg_rating", 3.0) / 5.0
    trust_score = predict_trust_score(input_data)
    trust_component = normalize(trust_score, 0, 100)
    distance_component = 1 - normalize(volunteer.get("distance_km", 0), 0, 20)
    experience_component = normalize(volunteer.get("completed_tasks", 0), 0, 200)
    elder_risk = risk_predict
    score = (
    MATCHING_WEIGHTS["trust_score"] * trust_component +
    MATCHING_WEIGHTS["distance"] * distance_component +
    MATCHING_WEIGHTS["availability"] * availability_score +
    MATCHING_WEIGHTS["experience"] * experience_component +
    0.2 * (1 - churn_prob) +
    0.2 * (1 - burnout_score) +
    0.1 * rating_score
)
    max_possible = sum(MATCHING_WEIGHTS.values()) + 0.2 + 0.2 + 0.1  
    score /= max_possible

    return round(score, 3), elder_risk, risk
def rank_volunteers(volunteers, elder_request):

    ranked_list = []
    for v in volunteers:
        score, elder_risk, risk = calculate_match_score(v, elder_request)
        if risk['decision'] == "BLOCK_ASSIGNMENT":
            continue

        ranked_list.append({
            "volunteer_id": v["id"],
            "match_score": score,
            "trust_score": v.get("trust_score", 0)
        })

    ranked_list.sort(key=lambda x: x["match_score"], reverse=True)
    return ranked_list

if __name__ == "__main__":
    volunteers = [
    { "id": 1, "completed_tasks": 20, "days_since_last_task": 1, "avg_rating": 4.8, "trust_score": 0.9, "cancellations": 0,
      "active_days": 40, "weekly_hours": 15, "consecutive_days": 3, "night_shifts": 1, "emergency_tasks": 2,
      "rest_days": 2, "distance_km": 2, "availability": "available" },

    { "id": 2, "completed_tasks": 5, "days_since_last_task": 10, "avg_rating": 3.5, "trust_score": 0.5, "cancellations": 1,
      "active_days": 15, "weekly_hours": 25, "consecutive_days": 6, "night_shifts": 3, "emergency_tasks": 1,
      "rest_days": 1, "distance_km": 5, "availability": "busy" },

    { "id": 3, "completed_tasks": 12, "days_since_last_task": 3, "avg_rating": 4.0, "trust_score": 0.7, "cancellations": 0,
      "active_days": 25, "weekly_hours": 12, "consecutive_days": 4, "night_shifts": 0, "emergency_tasks": 0,
      "rest_days": 3, "distance_km": 3.5, "availability": "available" },

    { "id": 4, "completed_tasks": 8, "days_since_last_task": 5, "avg_rating": 3.8, "trust_score": 0.6, "cancellations": 2,
      "active_days": 20, "weekly_hours": 18, "consecutive_days": 5, "night_shifts": 1, "emergency_tasks": 2,
      "rest_days": 2, "distance_km": 4, "availability": "available" },

    { "id": 5, "completed_tasks": 15, "days_since_last_task": 2, "avg_rating": 4.6, "trust_score": 0.85, "cancellations": 0,
      "active_days": 30, "weekly_hours": 10, "consecutive_days": 2, "night_shifts": 0, "emergency_tasks": 1,
      "rest_days": 3, "distance_km": 1.5, "availability": "available" },

    { "id": 6, "completed_tasks": 3, "days_since_last_task": 12, "avg_rating": 3.2, "trust_score": 0.4, "cancellations": 3,
      "active_days": 10, "weekly_hours": 20, "consecutive_days": 7, "night_shifts": 2, "emergency_tasks": 3,
      "rest_days": 1, "distance_km": 6, "availability": "busy" },

    { "id": 7, "completed_tasks": 18, "days_since_last_task": 2, "avg_rating": 4.7, "trust_score": 0.88, "cancellations": 1,
      "active_days": 35, "weekly_hours": 14, "consecutive_days": 3, "night_shifts": 1, "emergency_tasks": 2,
      "rest_days": 2, "distance_km": 2.2, "availability": "available" },

    { "id": 8, "completed_tasks": 7, "days_since_last_task": 8, "avg_rating": 3.6, "trust_score": 0.55, "cancellations": 2,
      "active_days": 18, "weekly_hours": 22, "consecutive_days": 5, "night_shifts": 2, "emergency_tasks": 1,
      "rest_days": 1, "distance_km": 5.5, "availability": "available" },

    { "id": 9, "completed_tasks": 10, "days_since_last_task": 4, "avg_rating": 4.1, "trust_score": 0.75, "cancellations": 0,
      "active_days": 25, "weekly_hours": 16, "consecutive_days": 3, "night_shifts": 1, "emergency_tasks": 2,
      "rest_days": 2, "distance_km": 3, "availability": "available" },

    { "id": 10, "completed_tasks": 2, "days_since_last_task": 15, "avg_rating": 3.0, "trust_score": 0.35, "cancellations": 4,
      "active_days": 8, "weekly_hours": 25, "consecutive_days": 7, "night_shifts": 3, "emergency_tasks": 3,
      "rest_days": 0, "distance_km": 7, "availability": "busy" }
    ]

    elder_request = {
    "age": 78,
    "chronic_disease": 1,
    "living_alone": 0,
    "mobility_issue": 1,
    "recent_fall": 0,
    "emergency_visits": 2
    }


    ranked_vols = rank_volunteers(volunteers, elder_request)
    print("Ranked Volunteers:")
    for v in ranked_vols:
        print(v)
