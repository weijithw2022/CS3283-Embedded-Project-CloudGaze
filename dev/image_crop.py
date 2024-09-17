import numpy as np
import cv2
import os
import matplotlib
matplotlib.use('TkAgg')


path = r'/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems Project/Project/images/output'
path_cropped = r'/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems Project/Project/images/cropped'

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in files:
    img_path = os.path.join(path, file)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    mask = np.zeros(img.shape[:2], dtype="uint8")
    center = (img.shape[1] // 2, img.shape[0] // 2)
    radius = 1500
    cv2.circle(mask, center, radius, 255, -1)
    masked_image = cv2.bitwise_and(img, img, mask=mask)

    x_start = center[0] - radius
    x_end = center[0] + radius
    y_start = center[1] - radius
    y_end = center[1] + radius

    cropped_image = masked_image[y_start:y_end, x_start:x_end]

    save_path = os.path.join(path_cropped, f'{os.path.splitext(file)[0]}_cropped.png')
    cv2.imwrite(save_path, cropped_image)
    print(f'Saved {save_path}')
