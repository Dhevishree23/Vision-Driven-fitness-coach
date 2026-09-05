import os
import pickle

MODEL_PATH = "models/fitness_model.pkl"

model = None

if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, "rb"))
    print("AI Model Loaded Successfully")
else:
    print("AI Model Not Found. Running without AI classification.")


def predict_form(angles):
    if model is None:
        return "Model Not Trained"

    prediction = model.predict([angles])
    return prediction[0]