import json

def save_motion(data):
    with open("data/user_motion.json", "w") as f:
        json.dump(data, f)