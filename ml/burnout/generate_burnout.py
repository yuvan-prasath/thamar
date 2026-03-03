import random
import pandas as pd

records = []

for _ in range(500):
    tasks_7 = random.randint(0, 15)
    tasks_30 = random.randint(tasks_7, 60)
    avg_duration = random.randint(20, 120)
    cancellations = random.randint(0, 6)
    days_no_break = random.randint(0, 40)

    burnout_score = (
        0.35 * (tasks_7 / 15) +
        0.25 * (tasks_30 / 60) +
        0.20 * (avg_duration / 120) +
        0.10 * (cancellations / 6) +
        0.10 * (days_no_break / 40)
    )

    burnout_score = min(round(burnout_score, 2), 1.0)

    records.append([
        tasks_7,
        tasks_30,
        avg_duration,
        cancellations,
        days_no_break,
        burnout_score
    ])

df = pd.DataFrame(records, columns=[
    "tasks_last_7_days",
    "tasks_last_30_days",
    "avg_task_duration",
    "cancellations",
    "days_since_last_break",
    "burnout_score"
])

df.to_csv("volunteer_burnout.csv", index=False)
print("Burnout dataset generated")
