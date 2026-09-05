import json

def correct_motion(input_file):

    with open(input_file) as f:
        data = json.load(f)

    corrected = []

    for frame in data:
        corrected_frame = [min(angle, 160) for angle in frame]
        corrected.append(corrected_frame)

    with open("data/corrected_motion.json", "w") as f:
        json.dump(corrected, f)

    return corrected