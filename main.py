import cv2
import mediapipe as mp
import numpy as np

# 🔥 ADD LOGGER
from phase5_data.data_logger import log_rep

from phase2_angles.angle_analysis import analyze_exercise
from phase3_reps.rep_counter import RepCounter
from phase4_fatigue.fatigue_tracker import FatigueTracker

# Safe AI import
try:
    from phase6_ai_form.multi_exercise_ai import predict_feedback
except:
    def predict_feedback(exercise, angles):
        return "AI Model Not Trained"

# Safe Forecast import
try:
    from phase8_forecasting_model.forecast_live import predict_future_status
except:
    def predict_future_status(angles):
        return "Forecast Model Not Trained"

from injury_risk_model import compute_injury_risk
from phase9_motion.video_corrector import display_correction


# ------------------ MEDIAPIPE INIT ------------------

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


# ------------------ EXERCISE SELECTION ------------------

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


# ------------------ INITIALIZE MODULES ------------------

rep_counter = RepCounter()
fatigue_tracker = FatigueTracker()

previous_reps = 0
rep_angles = []
last_feedback = ""
last_forecast = ""
last_injury = ""


# ------------------ CAMERA ------------------

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:

        landmarks = result.pose_landmarks.landmark
        angles = analyze_exercise(exercise, landmarks)

        if angles is not None and len(angles) > 0:

            primary_angle = angles[0]
            reps = rep_counter.update(primary_angle)

            rep_angles.append(angles)

            # -------- PER REP LOGIC --------
            if reps > previous_reps:

                previous_reps = reps

                rep_array = np.array(rep_angles)
                avg_angles = np.mean(rep_array, axis=0)

                # AI + Forecast + Injury
                last_feedback = predict_feedback(exercise, avg_angles.tolist())
                last_forecast = predict_future_status(avg_angles.tolist())
                last_injury = compute_injury_risk(avg_angles.tolist())

                # 🔥 SAVE DATA TO CSV
                log_rep(exercise, reps, avg_angles.tolist(), last_feedback)

                print("\n========== REP", reps, "==========")
                print("Exercise:", exercise)
                print("Angles:", [round(a, 2) for a in avg_angles])
                print("Command:", last_feedback)
                print("Forecast:", last_forecast)
                print("Injury Risk:", last_injury)
                print("==================================\n")

                rep_angles = []

            # -------- DISPLAY ON VIDEO --------

            cv2.putText(frame, f"Reps: {reps}",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            cv2.putText(frame, f"Angle: {round(primary_angle,1)}",
                        (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 0), 2)

            cv2.putText(frame, f"Command: {last_feedback}",
                        (30, 130),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)

            cv2.putText(frame, f"Forecast: {last_forecast}",
                        (30, 160),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 0, 0), 2)

            cv2.putText(frame, f"Injury: {last_injury}",
                        (30, 190),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 255), 2)

            # Correction overlay
            frame = display_correction(frame, last_feedback)

        mp_draw.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow("AI Fitness Coach", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()