import cv2
import cvzone
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

width = 106
height = 48

cap = cv2.VideoCapture("carPark.mp4")

# Initialize Firebase
cred = credentials.Certificate("Private_Key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parcar-dd9d9-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

prev_SpaceCounter = None

def checking_parking_space(imgPro):
    global prev_SpaceCounter
    SpaceCounter = 0
    slot_status_mapping = {}  # Dictionary to store slot occupancy status

    for i, pos in enumerate(posList):
        x, y = pos
        slot_number = i + 1
        imgcrop = imgPro[y:y+height, x:x+width]
        count = cv2.countNonZero(imgcrop)
        cvzone.putTextRect(img, str(count), (x,y+height-3), scale=1.1, thickness=2, offset=0)
        cvzone.putTextRect(img, str(slot_number), (x,y+height-30), scale=1, thickness=2, offset=0, colorR=(255, 0, 0))  # Draw slot number
        if count < 900:
            colour = (0, 255, 0)
            thickness = 5
            SpaceCounter += 1
            slot_status_mapping[slot_number] = 0  # Slot is empty

        else:
            colour = (0, 0, 255)
            thickness = 2
            slot_status_mapping[slot_number] = 1  # Slot is occupied
            
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), colour, thickness)
        
    cvzone.putTextRect(img, f'Free: {SpaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20)

    return slot_status_mapping

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    slot_status_mapping = checking_parking_space(imgDilate)
    cv2.imshow("frames", img)
    key = cv2.waitKey(4) & 0xFF
    if key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()
