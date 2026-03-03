import pandas as pd
import numpy as np
import joblib
import os


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from features import FEATURES , TARGET

np.random.seed(42)


data=pd.DataFrame(
    {
        "completed_tasks": np.random.randint(0, 100, 500),
    "cancelled_tasks": np.random.randint(0, 30, 500),
    "avg_response_time": np.random.uniform(1, 15, 500),
    "complaints_count": np.random.randint(0, 10, 500),
    "otp_failures": np.random.randint(0, 6, 500),
    "sos_triggers": np.random.randint(0, 3, 500),
    "background_verified": np.random.randint(0, 2, 500),
    "tenure_days": np.random.randint(1, 1000, 500),
    }
)

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

data[TARGET] = (
    40 * normalize(data["completed_tasks"])
    - 20 * normalize(data["cancelled_tasks"])
    - 15 * normalize(data["complaints_count"])
    - 10 * normalize(data["otp_failures"])
    - 10 * normalize(data["sos_triggers"])
    + 25 * data["background_verified"]
)


data[TARGET]=(100*(data[TARGET]-data[TARGET].min())/(data[TARGET].max()-data[TARGET].min()))

x=data[FEATURES]
y=data[TARGET]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

model=RandomForestRegressor(n_estimators=200,max_depth=10,random_state=42)

model.fit(x_train,y_train)

preds=model.predict(x_test)
mae=mean_absolute_error(y_test,preds)

print(f"mae = {mae:.2f}" )
print("preds ", preds)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(MODEL_DIR, "trust_model_v1.pkl")
joblib.dump(model, model_path)

print("Model saved at:", model_path)

