import cv2
import pickle
import cvzone
import numpy as np

# --- CONFIGURATION ---
VIDEO_PATH = 'carPark.mp4'
POS_FILE = 'CarParkPos'
WIDTH, HEIGHT = 107, 48
PIXEL_THRESHOLD = 900

# --- LOAD SLOTS ---
try:
    with open(POS_FILE, 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    print(f"[ERROR] File not found: {POS_FILE}")
    posList = []

# --- CHECK OCCUPANCY ---
def check_parking_space(img, img_pro):
    space_counter = 0

    for pos in posList:
        x, y = pos
        img_crop = img_pro[y:y+HEIGHT, x:x+WIDTH]
        count = cv2.countNonZero(img_crop)

        if count < PIXEL_THRESHOLD:
            color, thickness = (0, 255, 0), 5
            space_counter += 1
        else:
            color, thickness = (0, 0, 255), 2

        cv2.rectangle(img, pos, (x+WIDTH, y+HEIGHT), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y+HEIGHT-3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {space_counter}/{len(posList)}', (100, 50),
                       scale=3, thickness=5, offset=20, colorR=(0, 200, 0))

# --- MAIN LOOP ---
cap = cv2.VideoCapture(VIDEO_PATH)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        print("[ERROR] Couldn't read video frame.")
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    check_parking_space(img, img_dilate)

    cv2.imshow("Parking Monitor", img)
    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

