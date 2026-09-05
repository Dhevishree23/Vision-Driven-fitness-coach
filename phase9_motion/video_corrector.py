import cv2

def display_correction(frame, feedback):

    if "Lower" in feedback:
        cv2.putText(frame, "Correct: Lower Your Body",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3)

    elif "Straight" in feedback:
        cv2.putText(frame, "Correct: Keep Back Straight",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,255),
                    3)

    else:
        cv2.putText(frame, "Good Form",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    3)

    return frame