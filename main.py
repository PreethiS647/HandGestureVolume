import cv2
import mediapipe as mp
import numpy as np
import pyautogui

print("Starting Hand Volume Control...")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot access webcam")
    exit()

print("Webcam opened successfully")

prev_length = 0

while True:
    ret, img = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            x1, y1 = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)
            x2, y2 = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)

            length = np.hypot(x2 - x1, y2 - y1)

            if length > prev_length + 10:
                pyautogui.press("volumeup")

            elif length < prev_length - 10:
                pyautogui.press("volumedown")

            prev_length = length

    cv2.imshow("Hand Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()