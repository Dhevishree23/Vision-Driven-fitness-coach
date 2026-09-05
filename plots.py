import matplotlib.pyplot as plt

# ---------------- EXPERIMENTAL DATA ----------------
# Replace with your real collected results

reps = [1,2,3,4,5,6]

knee_angles = [65.69,77.33,78.72,47.58,72.39,55.67]
hip_angles = [163.57,78.32,143.61,125.52,192.52,177.65]
elbow_angles = [50.55,48.72,64.71,175.65,95.21,54.87]

injury_risk = [4,38,38,52,77,80]
skeletal_drift = [10.73,18.29,30.84,29.81,28.05,35.12]


# ---------------- PLOT SETTINGS ----------------

plt.figure(figsize=(12,8))


# ---------------- KNEE ANGLE GRAPH ----------------

plt.subplot(2,2,1)
plt.plot(reps,knee_angles,marker='o',linewidth=2)
plt.title("Knee Angle vs Repetition")
plt.xlabel("Repetition")
plt.ylabel("Knee Angle (degrees)")
plt.grid(True)


# ---------------- HIP ANGLE GRAPH ----------------

plt.subplot(2,2,2)
plt.plot(reps,hip_angles,marker='o',linewidth=2)
plt.title("Hip Angle vs Repetition")
plt.xlabel("Repetition")
plt.ylabel("Hip Angle (degrees)")
plt.grid(True)


# ---------------- INJURY RISK GRAPH ----------------

plt.subplot(2,2,3)
plt.plot(reps,injury_risk,marker='o',linewidth=2)
plt.title("Injury Risk vs Repetition")
plt.xlabel("Repetition")
plt.ylabel("Injury Risk (%)")
plt.grid(True)


# ---------------- SKELETAL DRIFT GRAPH ----------------

plt.subplot(2,2,4)
plt.plot(reps,skeletal_drift,marker='o',linewidth=2)
plt.title("Skeletal Drift vs Repetition")
plt.xlabel("Repetition")
plt.ylabel("Drift (degrees)")
plt.grid(True)


plt.tight_layout()
plt.show()