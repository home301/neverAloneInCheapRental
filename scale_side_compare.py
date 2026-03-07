import cv2
import numpy as np

img_path = r'd:\work_home\neverAloneInCheapRental\art\concepts\characters\ghost\05_fullbody_side.png'
out_path = r'C:\Users\cmk11\.gemini\antigravity\brain\f45ac83d-dcd0-4cdd-b903-04a09aad9bd6\ghost_Side_1_7x_comparison.png'

img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

if img is None:
    print(f"Could not load image from {img_path}")
    exit(1)

# Ensure white background logic
if len(img.shape) == 3 and img.shape[2] == 4:
    # If RGBA, make background white
    alpha_channel = img[:, :, 3]
    mask = alpha_channel < 250
    img[mask] = [255, 255, 255, 255]
    img = img[:, :, :3] # convert to BGR

# Get bounding box of character to find where the head starts
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Character is dark lines on white background
mask = gray < 240
y_indices, x_indices = np.where(mask)

if len(y_indices) == 0:
    print("Could not find character in image.")
    exit(1)

top_y = np.min(y_indices)
bottom_y = np.max(y_indices)
char_height = bottom_y - top_y

# Assume head is top 18% of the character height for the side view
head_ratio = 0.18
cut_y = int(top_y + char_height * head_ratio)

head_img = img[:cut_y, :]
body_img = img[cut_y:, :]

# Scale body vertically by 1.7
body_height = body_img.shape[0]
new_body_height = int(body_height * 1.7)

body_img_resized = cv2.resize(body_img, (body_img.shape[1], new_body_height), interpolation=cv2.INTER_LANCZOS4)

# Recombine 1.7x taller character
taller_img = np.vstack((head_img, body_img_resized))

# Now we want to lay them side by side, perfectly aligned at the bottom (feet).
orig_h, orig_w = img.shape[:2]
tall_h, tall_w = taller_img.shape[:2]

# The canvas needs to be tall enough for the taller image + some padding
canvas_h = tall_h + 50
canvas_w = orig_w + tall_w + 100

# Create pure white canvas
canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255

# Paste original image on the left, aligned to bottom
orig_start_y = canvas_h - orig_h - 20
canvas[orig_start_y:orig_start_y+orig_h, 20:20+orig_w] = img

# Paste taller image on the right, aligned to bottom
tall_start_y = canvas_h - tall_h - 20
canvas[tall_start_y:tall_start_y+tall_h, orig_w + 60:orig_w + 60 + tall_w] = taller_img

cv2.imwrite(out_path, canvas)
print(f"Saved precise 1.7x side-by-side comparison to {out_path}")
