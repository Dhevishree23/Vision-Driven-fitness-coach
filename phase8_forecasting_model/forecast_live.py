import torch
import os
import numpy as np

class ForecastLSTM(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = torch.nn.LSTM(2, 32, batch_first=True)
        self.fc = torch.nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out


MODEL_PATH = "models/forecast_model.pt"

model = None

if os.path.exists(MODEL_PATH):
    model = ForecastLSTM()
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
    print("Forecast Model Loaded Successfully")
else:
    print("Forecast Model Not Found. Running without Forecasting.")


sequence_buffer = []

def predict_future_status(current_angles):

    if model is None:
        return "Forecast Model Not Trained"

    sequence_buffer.append(current_angles)

    if len(sequence_buffer) < 5:
        return "Insufficient Data"

    seq = np.array(sequence_buffer[-5:])
    seq = torch.tensor(seq, dtype=torch.float32).unsqueeze(0)

    prediction = model(seq).item()

    if prediction > 170:
        return "Future Form Stable"
    elif prediction > 150:
        return "Form May Degrade"
    else:
        return "Take Rest Soon"