import random
import pandas as pd
records = []
for _ in range(500):
    tasks_completed = random.randint(0, 60)
    days_since_last_task = random.randint(0, 90)
    avg_rating = round(random.uniform(2.5, 5.0), 1)
    trust_score = round(random.uniform(0.2, 0.95), 2)
    cancellations = random.randint(0, 6)
    active_days = random.randint(10, 365)
    churn_probability = (
        0.4 * (days_since_last_task / 90) +
        0.3 * (cancellations / 6) +
        0.2 * (1 - trust_score) +
        0.1 * (1 - avg_rating / 5)
    )
    churn = 1 if churn_probability > random.uniform(0, 1) else 0
    records.append([
        tasks_completed,
        days_since_last_task,
        avg_rating,
        trust_score,
        cancellations,
        active_days,
        churn
    ])
columns = [
    "tasks_completed",
    "days_since_last_task",
    "avg_rating",
    "trust_score",
    "cancellations",
    "active_days",
    "churn"
]
df = pd.DataFrame(records, columns=columns)
df.to_csv("volunteer_churn.csv", index=False)
print("500 volunteer churn records generated successfully")