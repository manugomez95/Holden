# OBJETIVO MARCAR TAPETE CON EL CURSOR Y DEVOLVER COORDENADAS DE LA ESQUINA IZQUIERDA SUPERIOR DE LA PRIMERA CARTA

# import the necessary packages
from skimage import exposure
import numpy as np
import cv2

image = cv2.imread('img/pruebas/mesa2.png')

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# find the colors within the specified boundaries and apply
# the mask
lower = np.array([150], dtype = np.uint8)
upper = np.array([255], dtype = np.uint8)
mask = cv2.inRange(gray, lower, upper)
output = cv2.bitwise_and(gray, gray, mask = mask)
result = output

edged = cv2.Canny(result, 30, 200)

cv2.imshow("Cartas", edged)
cv2.waitKey()
cv2.destroyAllWindows()

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.05 * peri, True)

	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx

		# screenCnt[contorno][vertice][eje]
		screenCnt[0][0][0]

		cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

cv2.imshow("Cartas", image)
cv2.waitKey()
cv2.destroyAllWindows()
