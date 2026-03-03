import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report
import joblib
file_path = r"D:\thamar\thamar\ml\elders_risk\elder_risk.csv"
data = pd.read_csv(file_path)

x=data.drop("risk_level",axis=1)
y=data["risk_level"]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

model=RandomForestClassifier(n_estimators=200,random_state=42)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
print("accuracy : ",accuracy_score(y_test,y_pred))
print("Classification Score : ",classification_report(y_test,y_pred))

joblib.dump(model, "elder_risk_model.pkl")
