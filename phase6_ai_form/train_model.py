import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = pd.read_csv("data/fitness_data.csv")

X = data[["Angle1", "Angle2"]]
y = data["Status"]

model = RandomForestClassifier()
model.fit(X, y)

pickle.dump(model, open("models/fitness_model.pkl", "wb"))

print("Model Trained")