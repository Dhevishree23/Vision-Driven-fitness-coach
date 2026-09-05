import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load dataset
data = pd.read_csv("data/fitness_data.csv")

# We assume CSV has:
# Exercise, Angle1, Angle2, Status

X = data[["Exercise", "Angle1", "Angle2"]]
y = data["Status"]

# Convert exercise text to numeric
X["Exercise"] = X["Exercise"].astype("category").cat.codes

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
pickle.dump(model, open("models/multi_exercise.pkl", "wb"))

print("Multi Exercise Model Trained")