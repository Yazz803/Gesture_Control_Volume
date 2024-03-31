import cv2
import time
import numpy as np
import HandTrackingModule as htm  # Ensure this is properly implemented
import math
import subprocess  # For executing osascript
# import applescript
import osascript

################################
wCam, hCam = 100, 100
################################

cap = cv2.VideoCapture(0)  # Changed to 0, assuming you're using the built-in webcam. Adjust if necessary.
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
prev_volume_set_time = time.time() 

detector = htm.handDetector(detectionCon=0.5)

def get_volume():
    script = "output volume of (get volume settings)"
    process = subprocess.Popen(["osascript", "-e", script], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        print(f"Error: {error}")
    else:
        return int(output.strip())
    

current_volume = get_volume()
vol = 0
volBar = 400
volPer = current_volume

def set_volume(vol):
    # """Set macOS system volume."""
    # subprocess.run(["osascript", "-e", f"set volume output volume {vol}"])
    # applescript.AppleScript(f"set volume output volume {vol}").run()
    osascript.osascript(f"set volume output volume {vol}")


def volume_adjustment():
    """Periodically adjust the volume."""
    while True:
        current_volume = get_volume()
        set_volume(current_volume)
        time.sleep(0.1)  # Adjust volume every 1 second

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList[0]) != 0:
        x1, y1 = lmList[0][4][1], lmList[0][4][2]
        x2, y2 = lmList[0][8][1], lmList[0][8][2]
        x3, y3 = lmList[0][12][1], lmList[0][12][2]
        x4, y4 = lmList[0][16][1], lmList[0][16][2]
        x5, y5 = lmList[0][20][1], lmList[0][20][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x5, y5), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.line(img, (x2, y2), (x3, y3), (255, 0, 255), 3)
        cv2.line(img, (x3, y3), (x4, y4), (255, 0, 255), 3)
        cv2.line(img, (x4, y4), (x5, y5), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # Interpolate hand range to volume percentage (0-100)
        volPer = np.interp(length, [50, 300], [0, 100])
        volBar = np.interp(length, [50, 300], [400, 150])
        
        # Set volume (Note: macOS volume ranges from 0 to 100)
        # set_volume(volPer)
        # Set volume every 1 second
        if time.time() - prev_volume_set_time >= 1:
            # set_volume(volPer)
            prev_volume_set_time = time.time()
        print(int(length), volPer)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Volume Hand Control wak", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
