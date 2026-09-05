import numpy as np

class FatigueTracker:

    def __init__(self):
        self.rep_averages = []

    def update(self, rep_avg_angle):

        self.rep_averages.append(rep_avg_angle)

        if len(self.rep_averages) < 3:
            return "Normal"

        drift = self.rep_averages[-1] - self.rep_averages[-3]

        if drift > 10:
            return "WARNING: Form Degrading"

        if drift > 20:
            return "ALERT: Take Rest"

        return "Stable"