import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score
from sklearn.ensemble import RandomForestRegressor

file_path = r"D:\thamar\thamar\ml\burnout\volunteer_burnout.csv"
data = pd.read_csv(file_path)
x=data.drop("burnout_score",axis=1)
y=data["burnout_score"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

model=RandomForestRegressor(n_estimators=300,max_depth=8,random_state=42)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
print("Absolute error : ",mean_absolute_error(y_test,y_pred))
print("r2 score : ",r2_score(y_test,y_pred))

joblib.dump(model,"volunteer_burnout_model.pkl")
print("Model Saved Succcessfully")