import joblib
model_path="../elders_risk/elder_risk_model.pkl"
load_model=joblib.load(model_path)
elder_data=[[78,1,1,1,0,2]]
risk_predict=load_model.predict(elder_data)[0]
print("risk Pedict : ",risk_predict)           