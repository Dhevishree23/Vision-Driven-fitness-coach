import csv
import os

def log_rep(exercise, rep, angles, status):

    os.makedirs("data", exist_ok=True)
    file_path = "data/fitness_data.csv"

    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Exercise", "Rep", "Angle1", "Angle2", "Status"])

        writer.writerow([
            exercise,
            rep,
            round(angles[0], 2),
            round(angles[1], 2),
            status
        ])