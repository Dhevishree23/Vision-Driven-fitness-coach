import numpy as np

def compute_injury_risk(angles):

    risk_score = 0

    for angle in angles:

        if angle < 60:
            risk_score += 3
        elif angle < 90:
            risk_score += 2
        elif angle < 120:
            risk_score += 1

    if risk_score >= 5:
        return "HIGH RISK"
    elif risk_score >= 3:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"