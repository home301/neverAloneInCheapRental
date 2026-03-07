import cv2
import numpy as np
import os

img_path = r'd:\work_home\neverAloneInCheapRental\art\concepts\characters\ghost\04_fullbody_front.png'
out_path = r'C:\Users\cmk11\.gemini\antigravity\brain\f45ac83d-dcd0-4cdd-b903-04a09aad9bd6\ghost_taller_1_2x_python.png'

# Load image, preserving alpha channel if present
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

if img is None:
    print(f"Could not load image from {img_path}")
    exit(1)

# Find bounding box of the character
if len(img.shape) == 3 and img.shape[2] == 4:
    mask = img[:,:,3] > 0
elif len(img.shape) == 3:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = gray < 250
else:
    mask = img < 250

y_indices, x_indices = np.where(mask)
if len(y_indices) == 0:
    print("Could not find character in image.")
    exit(1)

top_y = np.min(y_indices)
bottom_y = np.max(y_indices)

char_height = bottom_y - top_y

# Assume head is top 22% of the character height. 
# We'll split the image at this point.
head_ratio = 0.22
cut_y = int(top_y + char_height * head_ratio)

head_img = img[:cut_y, :]
body_img = img[cut_y:, :]

# scale body vertically by 1.2
body_height = body_img.shape[0]
new_body_height = int(body_height * 1.2)

# Resize body using high-quality interpolation
body_img_resized = cv2.resize(body_img, (body_img.shape[1], new_body_height), interpolation=cv2.INTER_LANCZOS4)

# Combine head and new body
new_img = np.vstack((head_img, body_img_resized))
cv2.imwrite(out_path, new_img)
print(f"Saved manipulated image to {out_path}")
