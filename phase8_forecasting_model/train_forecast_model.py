import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import pickle


class ForecastLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=2, hidden_size=32, batch_first=True)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out


data = pd.read_csv("data/forecast_data.csv")

X = []
y = []

for i in range(len(data) - 5):
    seq = data.iloc[i:i+5][["Angle1","Angle2"]].values
    label = data.iloc[i+5]["Angle1"]
    X.append(seq)
    y.append(label)

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).view(-1,1)

model = ForecastLSTM()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(50):
    output = model(X)
    loss = criterion(output, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), "models/forecast_model.pt")
print("Forecast Model Trained")