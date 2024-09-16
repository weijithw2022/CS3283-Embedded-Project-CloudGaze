import cv2
import os
from skimage.exposure import histogram, cumulative_distribution
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

path = r'/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems Project/Project/images/output/IMG_1813.jpg'
dir = r'/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems Project/Project/images/gray'
img = cv2.imread(path, cv2.IMREAD_COLOR)
gray_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
name = '/IMG_1813.jpg'
cv2.imwrite(f'{dir}{name}', gray_image)
freq, bins = histogram(gray_image)
plt.step(bins, freq*1.0/freq.sum())
plt.xlabel('intensity value')
plt.ylabel('fraction of pixels')
plt.show()