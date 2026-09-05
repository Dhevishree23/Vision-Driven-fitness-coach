import pickle
import os
import numpy as np

MODEL_PATH = "models/multi_exercise.pkl"

model = None

if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, "rb"))
    print("Multi Exercise Model Loaded")
else:
    print("Multi Exercise Model Not Found")

exercise_map = {
    "squat": 0,
    "pushup": 1,
    "lunge": 2,
    "plank": 3
}

def predict_feedback(exercise, angles):

    if model is None:
        return "Model Not Trained"

    ex_code = exercise_map[exercise]
    input_data = [[ex_code] + angles]

    prediction = model.predict(input_data)
    return prediction[0]