import numpy as np

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6
    )

    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle


def analyze_exercise(exercise, landmarks):

    def pt(i):
        return [landmarks[i].x, landmarks[i].y]

    import mediapipe as mp
    mp_pose = mp.solutions.pose

    if exercise == "squat":
        hip = pt(mp_pose.PoseLandmark.LEFT_HIP.value)
        knee = pt(mp_pose.PoseLandmark.LEFT_KNEE.value)
        ankle = pt(mp_pose.PoseLandmark.LEFT_ANKLE.value)
        shoulder = pt(mp_pose.PoseLandmark.LEFT_SHOULDER.value)

        knee_angle = calculate_angle(hip, knee, ankle)
        back_angle = calculate_angle(shoulder, hip, knee)
        return [knee_angle, back_angle]

    if exercise == "pushup":
        shoulder = pt(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
        elbow = pt(mp_pose.PoseLandmark.LEFT_ELBOW.value)
        wrist = pt(mp_pose.PoseLandmark.LEFT_WRIST.value)
        hip = pt(mp_pose.PoseLandmark.LEFT_HIP.value)
        ankle = pt(mp_pose.PoseLandmark.LEFT_ANKLE.value)

        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        body_angle = calculate_angle(shoulder, hip, ankle)
        return [elbow_angle, body_angle]

    if exercise == "plank":
        shoulder = pt(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
        hip = pt(mp_pose.PoseLandmark.LEFT_HIP.value)
        ankle = pt(mp_pose.PoseLandmark.LEFT_ANKLE.value)

        body_angle = calculate_angle(shoulder, hip, ankle)
        return [body_angle]

    if exercise == "lunge":
        hip = pt(mp_pose.PoseLandmark.LEFT_HIP.value)
        knee = pt(mp_pose.PoseLandmark.LEFT_KNEE.value)
        ankle = pt(mp_pose.PoseLandmark.LEFT_ANKLE.value)
        shoulder = pt(mp_pose.PoseLandmark.LEFT_SHOULDER.value)

        knee_angle = calculate_angle(hip, knee, ankle)
        torso_angle = calculate_angle(shoulder, hip, knee)
        return [knee_angle, torso_angle]