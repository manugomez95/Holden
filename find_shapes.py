import numpy as np
import cv2

# gama de blancos pertenecientes a una carta (en escala RGB)
COLOR_MIN = 150
COLOR_MAX = 255
# ratio altura/anchura de un rectangulo para identificarlo como carta
RATIO_MIN = 1.3
RATIO_MAX = 1.7

# input: 	imagen de la mesa
# output: 	posiciones de las cartas (vertices izquierdos superiores) (array de ints)
#			altura media	(int)
#			anchura media (int)
def reconocer_mesa(image):
	# TRATAMIENTO DE LA IMAGEN
	# se convierte la imagen a blanco y negro
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	# se le pasa un filtro para eliminar ruido de la imagen
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	
	# se aplica una mascara que filtre los colores
	# para que resalten los blancos
	lower = np.array([COLOR_MIN], dtype = np.uint8)
	upper = np.array([COLOR_MAX], dtype = np.uint8)
	mask = cv2.inRange(gray, lower, upper)
	output = cv2.bitwise_and(gray, gray, mask = mask)
	result = output
	
	# se detectan bordes mediante la funcion canny
	edged = cv2.Canny(result, 30, 200)

	# imagen tratada
	#cv2.imshow("Cartas", edged)
	#cv2.waitKey()
	#cv2.destroyAllWindows()

	# ahora buscamos contornos/formas dentro de la imagen
	_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# se guarda en memoria los 20 contornos mas grandes
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
	screenCnt = None

	posiciones_cartas = [] # esquinas superiores izquierdas de cada carta
	alturas = np.array([]) # alto de cada carta localizada
	anchuras = np.array([]) # ancho de cada carta localizada

	# para cada contorno
	for c in cnts:
		# se aproxima el contorno
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
			# segundo filtro, tiene forma de carta?
			if ratio>RATIO_MIN and ratio<RATIO_MAX:
				posiciones_cartas.append(izq_sup[0])
				alturas = np.append(alturas, alto)
				anchuras = np.append(anchuras, ancho)
				# dibuja el contorno en verde en la imagen original
				cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

	altura_media = round(np.mean(alturas))
	anchura_media = round(np.mean(anchuras))
	posiciones_cartas.sort()

	# resultado
	cv2.imshow("Cartas", image)
	cv2.waitKey()
	cv2.destroyAllWindows()

	return posiciones_cartas, altura_media, anchura_media

################## CODIGO QUE SE EJECUTA #########################
image = cv2.imread('img/pruebas/mesa.png')
reconocer_mesa(image)
