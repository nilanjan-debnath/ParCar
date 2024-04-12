import cv2
import pickle

cap = cv2.VideoCapture(1)
# cap.set(3, 640)
# cap.set(4, 480)

# while True:
#     sucess, img = cap.read()
#     cv2.imshow("vid", img)
#     cv2.waitKey(1)

# width = 180
# height = 440

width = 200
height = 110

try:
    with open('TestingPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouse_click (events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('TestingPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # cv2.rectangle(img, (50,193), (156,145), (255,0,255), 2)
    # cv2.rectangle(img, (30, 430), (220, 20), (255, 0, 255), 2)
    # img = cv2.imread("parkingImg.jpg")
    sucess, img = cap.read()
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouse_click)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):  # Break the loop if 'Q' or 'q' is pressed
        break
