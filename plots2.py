import matplotlib.pyplot as plt
import numpy as np

# ---------------- SAMPLE DATA ----------------
# Replace these values with your real collected results

reps = [1,2,3,4,5,6]

knee_angles = [65.69,77.33,78.72,47.58,72.39,55.67]
hip_angles = [163.57,78.32,143.61,125.52,192.52,177.65]
elbow_angles = [50.55,48.72,64.71,175.65,95.21,54.87]

fatigue_score = [10,25,35,52,77,88]
form_score = [90,85,80,76,72,68]

# ROM values calculated from workout
knee_rom = max(knee_angles) - min(knee_angles)
hip_rom = max(hip_angles) - min(hip_angles)
elbow_rom = max(elbow_angles) - min(elbow_angles)

# Workout efficiency example
efficiency = [f * 0.8 for f in form_score]

# ---------------- REAL-TIME PERFORMANCE DASHBOARD ----------------

plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.plot(reps,knee_angles,marker='o',linewidth=2)
plt.title("Real-Time Knee Angle Performance")
plt.xlabel("Repetition")
plt.ylabel("Angle (degrees)")
plt.grid(True)

plt.subplot(2,2,2)
plt.plot(reps,hip_angles,marker='o',linewidth=2)
plt.title("Real-Time Hip Angle Performance")
plt.xlabel("Repetition")
plt.ylabel("Angle (degrees)")
plt.grid(True)

plt.subplot(2,2,3)
plt.plot(reps,form_score,marker='o',linewidth=2)
plt.title("Form Score Tracking")
plt.xlabel("Repetition")
plt.ylabel("Form Score")
plt.grid(True)

plt.subplot(2,2,4)
plt.plot(reps,efficiency,marker='o',linewidth=2)
plt.title("Workout Efficiency")
plt.xlabel("Repetition")
plt.ylabel("Efficiency Score")
plt.grid(True)

plt.tight_layout()
plt.show()

# ---------------- ROM ANALYSIS GRAPH ----------------

joints = ["Knee","Hip","Elbow"]
rom_values = [knee_rom, hip_rom, elbow_rom]

plt.figure()
plt.bar(joints, rom_values)
plt.title("Range of Motion (ROM) Analysis")
plt.ylabel("Degrees")
plt.xlabel("Joint")
plt.show()

# ---------------- FATIGUE PREDICTION CURVE ----------------

plt.figure()
plt.plot(reps,fatigue_score,marker='o',linewidth=2)
plt.title("Fatigue Prediction Curve")
plt.xlabel("Repetition")
plt.ylabel("Fatigue Score")
plt.grid(True)
plt.show()

# ---------------- WORKOUT EFFICIENCY CHART ----------------

plt.figure()
plt.plot(reps,efficiency,marker='o',linewidth=2)
plt.title("Workout Efficiency Over Reps")
plt.xlabel("Repetition")
plt.ylabel("Efficiency")
plt.grid(True)
plt.show()