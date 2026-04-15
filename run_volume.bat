@echo off
cd /d C:\Users\admin\Desktop\HandGestureVolume
"C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe" main.py
pauseimport cv2

cap = cv2.VideoCapture(0)

print("Program started")
print("Camera opened:", cap.isOpened())

while True:
    success, frame = cap.read()

    if not success:
        break

    cv2.imshow("Hand Gesture Volume", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()