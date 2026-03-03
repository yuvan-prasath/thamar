from burnout_churn import predict_combined_risk

volunteer = {
    "tasks_completed": 12,
    "days_since_last_task": 3,
    "avg_rating": 4.2,
    "trust_score": 0.78,
    "cancellations": 1,
    "active_days": 120,

    "weekly_hours": 18,
    "consecutive_days": 5,
    "night_shifts": 1,
    "emergency_tasks": 2,
    "rest_days": 2
}

result = predict_combined_risk(volunteer)
print(result)
