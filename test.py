import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

print("Program started")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera failed")
    exit()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

print("System Ready")

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append((cx, cy))

        if len(lmList) >= 9:
            x1, y1 = lmList[4]
            x2, y2 = lmList[8]

            cv2.circle(img,(x1,y1),10,(0,255,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(0,255,0),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

            length = math.hypot(x2-x1, y2-y1)

            vol = np.interp(length,[30,200],[minVol,maxVol])
            volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Hand Gesture Volume", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()