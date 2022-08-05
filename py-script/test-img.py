import cv2
import numpy as np

img = 66 * np.ones((100, 100, 3))
cv2.imshow("show", img)
cv2.waitKey()
cv2.namedWindow("show", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("show", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
