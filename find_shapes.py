# OBJETIVO MARCAR TAPETE CON EL CURSOR Y DEVOLVER COORDENADAS DE LA ESQUINA IZQUIERDA SUPERIOR DE LA PRIMERA CARTA

# import the necessary packages
from skimage import exposure
import numpy as np
import cv2

# ratio altura/anchura de un rectangulo para reconocer cartas
RATIO_MIN = 1.3
RATIO_MAX = 1.7

# input: imagen de la mesa
# output: posiciones de las cartas, altura media, anchura media
def reconocer_mesa(image):
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
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
	screenCnt = None

	posiciones_cartas = []
	alturas = np.array([])
	anchuras = np.array([])

	# loop over our contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.05 * peri, True)
		# si el contorno tiene 4 lados pasa el primer filtro
		if len(approx) == 4:
			screenCnt = approx
			izq_sup = screenCnt[0][0][:]
			der_inf = screenCnt[2][0][:]
			alto = der_inf[1] - izq_sup[1]
			ancho = der_inf[0] - izq_sup[0]
			ratio = alto/ancho
			# segundo filtro, ¿tiene forma de carta?
			if ratio>RATIO_MIN and ratio<RATIO_MAX:
				posiciones_cartas.append(izq_sup[0])
				alturas = np.append(alturas, alto)
				anchuras = np.append(anchuras, ancho)
				cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

	altura_media = round(np.mean(alturas))
	anchura_media = round(np.mean(anchuras))
	posiciones_cartas.sort()
	print(posiciones_cartas)
	print(altura_media)
	print(anchura_media)

	cv2.imshow("Cartas", image)
	cv2.waitKey()
	cv2.destroyAllWindows()

	return posiciones_cartas, altura_media, anchura_media

image = cv2.imread('img/pruebas/mesa.png')
reconocer_mesa(image)
