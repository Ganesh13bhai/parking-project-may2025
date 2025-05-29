import cv2
import pickle
import numpy as np
import pandas as pd

# --- CONFIGURATION ---
VIDEO_PATH = 'carPark.mp4'
POS_FILE = 'CarParkPos'
WIDTH, HEIGHT = 107, 48
PIXEL_THRESHOLD = 900

# --- LOAD PARKING SLOTS ---
with open(POS_FILE, 'rb') as f:
    posList = pickle.load(f)

# --- PROCESS FRAME ---
cap = cv2.VideoCapture(VIDEO_PATH)
success, img = cap.read()
cap.release()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 25, 16)
img_median = cv2.medianBlur(img_thresh, 5)
kernel = np.ones((3, 3), np.uint8)
img_dilate = cv2.dilate(img_median, kernel, iterations=1)

# --- COUNT OCCUPANCY ---
occupied = 0
for x, y in posList:
    crop = img_dilate[y:y + HEIGHT, x:x + WIDTH]
    count = cv2.countNonZero(crop)
    if count >= PIXEL_THRESHOLD:
        occupied += 1

total_slots = len(posList)
available = total_slots - occupied

# --- EXPORT CSV ---
df = pd.DataFrame([{
    "Total Slots": total_slots,
    "Occupied Slots": occupied,
    "Available Slots": available
}])
df.to_csv("results/parking_status.csv", index=False)

print("[✓] CSV exported: results/parking_status.csv")

