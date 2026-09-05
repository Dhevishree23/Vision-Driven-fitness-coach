import cv2
import mediapipe as mp
import numpy as np
import os
from collections import deque
import random
import time
from voice_coach import speak
motivation_messages = [ "Great job, keep going", 
                       "Nice rep, stay focused", 
                       "Perfect, maintain the rhythm",
                       "Good control, continue", 
                       "Excellent form, keep pushing",
                         "You are doing great", 
                         "Stay strong", ]

# ---------------- INIT ----------------

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# ---------------- HISTORY FOR FORECASTING ----------------

knee_history = deque(maxlen=30)
hip_history = deque(maxlen=30)
elbow_history = deque(maxlen=30)

# ---------------- ANGLE FUNCTION ----------------

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle

# ---------------- REP COUNTER ----------------

class RepCounter:

    def __init__(self):
        self.stage = None
        self.counter = 0

    def update(self, angle, up_thresh=160, down_thresh=80):

        if angle > up_thresh:
            self.stage = "up"

        if angle < down_thresh and self.stage == "up":
            self.stage = "down"
            self.counter += 1

        return self.counter

# ---------------- INTELLIGENT FEEDBACK ----------------

def intelligent_feedback(exercise, knee, hip, elbow):

    feedback = []

    if exercise == "squat":

        if knee > 165:
            feedback.append("Lower your hips slightly")

        if abs(knee - hip) > 40:
            feedback.append("Keep knees aligned with toes")

        spine_dev = abs(hip - 180)

        if spine_dev > 5:
            feedback.append(f"Straighten spine by {round(spine_dev,1)} degrees")

        if len(knee_history) > 10 and np.std(knee_history) > 20:
            feedback.append("Move slower to maintain balance")

    elif exercise == "pushup":

        if elbow > 160:
            feedback.append("Lower your chest")

        if elbow < 70:
            feedback.append("Push up fully")

        if hip < 160:
            feedback.append("Keep body straight")

    elif exercise == "lunge":

        if knee > 150:
            feedback.append("Step forward slightly")

        if knee < 80:
            feedback.append("Do not go too deep")

        if abs(knee - hip) > 35:
            feedback.append("Align knee with toes")

    elif exercise == "plank":

        if hip < 160:
            feedback.append("Lift hips slightly")

        if hip > 190:
            feedback.append("Lower hips")

        if abs(hip - 180) > 10:
            feedback.append("Keep spine neutral")

    if not feedback:
        feedback.append("Good Form")

    return feedback

# ---------------- MOTION FORECASTING ----------------

def motion_forecasting(exercise):

    if len(knee_history) < 15:
        return None

    # Normalize variance
    knee_var = min(30, np.var(knee_history))
    hip_var = min(30, np.var(hip_history))
    elbow_var = min(30, np.var(elbow_history))

    # skeletal drift
    drift = np.std(knee_history)

    fatigue = []

    if exercise == "squat":

        if knee_var > 15:
            fatigue.append("knees")

        if hip_var > 15:
            fatigue.append("lower back")

    elif exercise == "pushup":

        if elbow_var > 15:
            fatigue.append("shoulders")

        if hip_var > 15:
            fatigue.append("core")

    elif exercise == "lunge":

        if knee_var > 15:
            fatigue.append("knees")

        if hip_var > 15:
            fatigue.append("glutes")

    elif exercise == "plank":

        if hip_var > 15:
            fatigue.append("core")

        if elbow_var > 15:
            fatigue.append("shoulders")

    if not fatigue:
        fatigue.append("none")

#--------- FATIGUE SCORE --------

    fatigue_score = (knee_var + hip_var + elbow_var) / 3

    fatigue_score = (fatigue_score / 30) * 100
    fatigue_score = min(100, fatigue_score)

    # -------- REP FAILURE PREDICTION --------

    if fatigue_score < 20:
        reps_left = random.randint(10, 15)

    elif fatigue_score < 40:
        reps_left = random.randint(6, 10)

    elif fatigue_score < 60:
        reps_left = random.randint(4, 6)

    elif fatigue_score < 80:
        reps_left = random.randint(2, 4)

    else:
        reps_left = random.randint(1, 2)

    risk = int(fatigue_score)

    return {
        "fail": f"Your form will likely fail after {reps_left} more reps",
        "drift": f"Predicted skeletal drift: {round(drift,2)} degrees",
        "fatigue": f"Predicted fatigue areas: {', '.join(fatigue)}",
        "injury": f"Forecasted injury risk score: {risk}%"
    }

def generate_personalized_plan(exercise, knee_rom, hip_rom, elbow_rom, score):

    corrective = []
    mobility = []
    daily_plan = []

    # ---------------- SQUAT PLAN ----------------
    if exercise == "squat":

        if knee_rom < 80:
            corrective.append("Goblet Squats – 3 sets x 10 reps")
            corrective.append("Box Squats – 3 sets x 8 reps")

            mobility.append("Hip Flexor Stretch – 30 seconds x 3")
            mobility.append("Ankle Mobility Drill – 10 reps x 3")

        if hip_rom < 40:
            mobility.append("Glute Bridge – 3 sets x 12 reps")

        daily_plan = [
            "Day 1 – Slow tempo squats",
            "Day 2 – Hip mobility drills",
            "Day 3 – Core strengthening",
            "Day 4 – Squat training repeat"
        ]

    # ---------------- PUSHUP PLAN ----------------
    elif exercise == "pushup":

        if elbow_rom < 90:
            corrective.append("Incline Pushups – 3 sets x 10 reps")
            corrective.append("Knee Pushups – 3 sets x 12 reps")

        mobility.append("Shoulder Stretch – 30 seconds x 3")
        mobility.append("Chest Opener Stretch – 30 seconds")

        daily_plan = [
            "Day 1 – Pushup form training",
            "Day 2 – Shoulder mobility drills",
            "Day 3 – Triceps strengthening",
            "Day 4 – Pushup training repeat"
        ]

    # ---------------- LUNGE PLAN ----------------
    elif exercise == "lunge":

        if knee_rom < 70:
            corrective.append("Reverse Lunges – 3 sets x 10 reps")

        mobility.append("Hip Mobility Stretch – 30 seconds")
        mobility.append("Hamstring Stretch – 30 seconds")

        daily_plan = [
            "Day 1 – Lunge technique practice",
            "Day 2 – Hip mobility training",
            "Day 3 – Balance exercises",
            "Day 4 – Lunge training repeat"
        ]

    # ---------------- PLANK PLAN ----------------
    elif exercise == "plank":

        corrective.append("Side Plank – 3 sets x 30 seconds")
        corrective.append("Dead Bug Core Drill – 3 sets x 10")

        mobility.append("Lower Back Stretch – 30 seconds")
        mobility.append("Cat Cow Stretch – 10 reps")

        daily_plan = [
            "Day 1 – Plank endurance training",
            "Day 2 – Core mobility",
            "Day 3 – Stability training",
            "Day 4 – Plank repeat"
        ]

    return corrective, mobility, daily_plan

# ---------------- AI TRAINING RECOMMENDATIONS ----------------

def generate_training_recommendations(exercise, knee_rom, hip_rom, elbow_rom, fatigue_score):

    recommendations = []

    if exercise == "squat":

        if knee_rom < 80:
            recommendations.append("Improve squat depth with hip mobility drills")

        if hip_rom < 40:
            recommendations.append("Work on hip flexibility and glute activation")

        if fatigue_score > 70:
            recommendations.append("Take longer rest between squat sets")

    elif exercise == "pushup":

        if elbow_rom < 90:
            recommendations.append("Focus on full push up depth")

        if fatigue_score > 70:
            recommendations.append("Strengthen triceps and shoulder endurance")

    elif exercise == "lunge":

        if knee_rom < 70:
            recommendations.append("Practice deeper lunges for better mobility")

        if hip_rom < 40:
            recommendations.append("Improve hip stability with balance drills")

    elif exercise == "plank":

        if hip_rom > 20:
            recommendations.append("Work on core stability to reduce hip movement")

        if fatigue_score > 60:
            recommendations.append("Add core endurance training")

    if fatigue_score > 80:
        recommendations.append("Reduce workout intensity to prevent injury")

    if len(recommendations) == 0:
        recommendations.append("Great performance. Maintain this training routine")

    return recommendations

    

def compute_form_score(knee, hip, elbow):

    score = 100

    if abs(180 - hip) > 10:
        score -= 15

    if abs(knee - hip) > 40:
        score -= 15

    if elbow < 60 or elbow > 170:
        score -= 10

    return max(score, 50)

# ---------------- SELECT EXERCISE ----------------

print("\nSelect Exercise:")
print("1 - Squat")
print("2 - Pushup")
print("3 - Lunge")
print("4 - Plank")

choice = input("Enter number: ")

exercise_map = {
    "1": "squat",
    "2": "pushup",
    "3": "lunge",
    "4": "plank"
}

exercise = exercise_map.get(choice, "squat")

print("Selected:", exercise)
speak(f"Starting {exercise} exercise. Let's begin.")
 

# ---------------- VIDEO OUTPUT ----------------

os.makedirs("corrected_videos", exist_ok=True)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    f"corrected_videos/{exercise}_corrected.mp4",
    fourcc,
    20.0,
    (640, 480)
)

rep_counter = RepCounter()
previous_reps = 0
total_reps = 0
form_scores = []
start_time = time.time()

cap = cv2.VideoCapture(0)
# ---------------- ROM TRACKING ----------------

knee_min = float('inf')
knee_max = float('-inf')

hip_min = float('inf')
hip_max = float('-inf')

elbow_min = float('inf')
elbow_max = float('-inf')

# ---------------- MAIN LOOP ----------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(rgb)

    if result.pose_landmarks:

        landmarks = result.pose_landmarks.landmark

        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h]

        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * w,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * h]

        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * w,
                 landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h]

        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]

        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]

        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

        knee_angle = calculate_angle(hip, knee, ankle)
        hip_angle = calculate_angle(shoulder, hip, knee)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        # ---------------- UPDATE ROM ----------------

        if knee_angle > 0:
            knee_min = min(knee_min, knee_angle)
            knee_max = max(knee_max, knee_angle)

        if hip_angle > 0:
            hip_min = min(hip_min, hip_angle)
            hip_max = max(hip_max, hip_angle)

        if elbow_angle > 0:
            elbow_min = min(elbow_min, elbow_angle)
            elbow_max = max(elbow_max, elbow_angle) 

        knee_history.append(knee_angle)
        hip_history.append(hip_angle)
        elbow_history.append(elbow_angle)

        primary_angle = knee_angle if exercise in ["squat", "lunge"] else elbow_angle

        reps = rep_counter.update(primary_angle)

        feedback_list = intelligent_feedback(exercise, knee_angle, hip_angle, elbow_angle)

        if reps > previous_reps:

            previous_reps = reps
            total_reps += 1

            rep_score = compute_form_score(knee_angle, hip_angle, elbow_angle)

            form_scores.append(rep_score)

            print("\n========== REP", reps, "==========")
            print("Exercise:", exercise)
            print("Knee Angle:", round(knee_angle,2))
            print("Hip Angle:", round(hip_angle,2))
            print("Elbow Angle:", round(elbow_angle,2))

            for msg in feedback_list:
                print("Feedback:", msg)


            # Motivation from AI coach
            motivation = random.choice(motivation_messages)
            print("Coach:", motivation)

            forecast = motion_forecasting(exercise)

            if forecast:

                print("\n===== MOTION FORECAST =====")
                print(forecast["fail"])
                print(forecast["drift"])
                print(forecast["fatigue"])
                print(forecast["injury"])
                print("===========================")
                

        mp_draw.draw_landmarks(frame,
                               result.pose_landmarks,
                               mp_pose.POSE_CONNECTIONS)

        cv2.putText(frame, f"Reps: {reps}", (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(frame, f"Knee Angle: {round(knee_angle,1)}", (20,100),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

        cv2.putText(frame, f"Hip Angle: {round(hip_angle,1)}", (20,130),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

        cv2.putText(frame, f"Elbow Angle: {round(elbow_angle,1)}", (20,160),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

        for i,msg in enumerate(feedback_list):
            cv2.putText(frame,msg,(20,220+i*30),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

        black = np.zeros_like(frame)

        mp_draw.draw_landmarks(black,
                               result.pose_landmarks,
                               mp_pose.POSE_CONNECTIONS)

        cv2.putText(black, f"Reps: {reps}", (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(black, f"Knee Angle: {round(knee_angle,1)}", (20,100),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

        cv2.putText(black, f"Hip Angle: {round(hip_angle,1)}", (20,130),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

        cv2.putText(black, f"Elbow Angle: {round(elbow_angle,1)}", (20,160),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

        for i,msg in enumerate(feedback_list):
            cv2.putText(black,msg,(20,220+i*30),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

        out.write(black)

    cv2.imshow("AI Vision Fitness Coach", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- WORKOUT ANALYTICS ----------------

end_time = time.time()
duration = (end_time - start_time) / 60

avg_score = int(np.mean(form_scores)) if form_scores else 0

# simple calorie estimation
calories = round(total_reps * 0.32 + duration * 3.5, 2)

# ---------------- CALCULATE ROM ----------------

knee_rom = round(abs(knee_max - knee_min), 2) if knee_max != float('-inf') else 0
hip_rom = round(abs(hip_max - hip_min), 2) if hip_max != float('-inf') else 0
elbow_rom = round(abs(elbow_max - elbow_min), 2) if elbow_max != float('-inf') else 0

#-----------------WORKOUT SUMMARY---------------

print("\n========== WORKOUT SUMMARY ==========")
print("Total Reps:", total_reps)
print("Workout Score:", avg_score, "/ 100")
print("Calories Burned:", calories, "kcal")
print("Duration:", round(duration,2), "minutes")
print("=====================================\n")

print("\n------ RANGE OF MOTION ------")
print("Knee ROM:", knee_rom, "degrees")
print("Hip ROM:", hip_rom, "degrees")
print("Elbow ROM:", elbow_rom, "degrees")
print("-----------------------------")


corrective, mobility, daily_plan = generate_personalized_plan(
    exercise,
    knee_rom,
    hip_rom,
    elbow_rom,
    avg_score
)

print("\n========== PERSONALIZED TRAINING PLAN ==========")

print("\nCorrective Exercises")
for c in corrective:
    print("-", c)
    speak(c)

print("\nMobility and Stretching Drills")
for m in mobility:
    print("-", m)
    speak(m)

print("\nDaily Plan for Form Improvement")
for d in daily_plan:
    print("-", d)
    speak(d)

print("\n===============================================")

# ---------------- AI TRAINING RECOMMENDATIONS ----------------

fatigue_score = int((np.var(knee_history) + np.var(hip_history) + np.var(elbow_history)) / 3)

recommendations = generate_training_recommendations(
    exercise,
    knee_rom,
    hip_rom,
    elbow_rom,
    fatigue_score
)

print("\n===== AI TRAINING RECOMMENDATIONS =====")

for rec in recommendations:
    print("-", rec)
    speak(rec)

print("=======================================")




cap.release()
out.release()
cv2.destroyAllWindows()
