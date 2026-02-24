import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial
import time


arduino = serial.Serial('COM5', 9600)  
time.sleep(2)
model_path = "hand_landmarker.task"

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]
def to_pixel(x,y,w,h):
    x = min(max(x,0.0),1.0)
    y = min(max(y,0.0),1.0)
    return int(x*w), int(y*h)

def draw_hand(image, hand_landmarks):
    h,w,_ = image.shape
    pts = [to_pixel(lm.x, lm.y, w, h) for lm in hand_landmarks]

    for a,b in HAND_CONNECTIONS:
        cv2.line(image, pts[a], pts[b], (0,255,0), 2)
    for x,y in pts:
        cv2.circle(image,(x,y),4,(0,0,255),-1)
    return pts

def thumb_up(pts):
    return 1 if pts[4][0] < pts[3][0] else 0

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    running_mode=vision.RunningMode.VIDEO
)
landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    import time
    timestamp = int(time.time()*1000)

    result = landmarker.detect_for_video(mp_image, timestamp)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            pts = draw_hand(frame, hand_landmarks)
            val = thumb_up(pts) 
            arduino.write(f"{val}\n".encode()) 
            cv2.putText(frame,f'Thumb: {val}',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("AI Robot Arm", frame)
    if cv2.waitKey(1) & 0xFF==27: break

cap.release()
cv2.destroyAllWindows()
arduino.close()
