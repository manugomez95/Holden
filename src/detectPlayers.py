import cv2
import numpy as np
from importlib import reload
import utils
from detectTableCards import *
import pytesseract
from scipy.spatial import distance

reload(utils)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

# TODO - hacer robusto a cambios de resolucion
def findTextNearPerimeter(im, outer_perimeter, inner_perimeter, DEBUG=False):
	[x_o, y_o, w_o, h_o] = outer_perimeter
	[x_i, y_i, w_i, h_i] = inner_perimeter

	if DEBUG: mock = im.copy()

	# apply grayscale
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	# morphological gradient
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))	# MUY INTERESANTE
	grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, morph_kernel)
	_, bw = cv2.threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
	# connect horizontally oriented regions
	connected = cv2.morphologyEx(bw, cv2.MORPH_OPEN, morph_kernel, iterations=1)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 3))
	connected = cv2.morphologyEx(connected, cv2.MORPH_CLOSE, morph_kernel, iterations=6)
	# find contours
	_, contours, hierarchy = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:35]
	# filter contours
	players = []
	while contours:
		cnt = contours.pop()
		[x, y, w, h] = cv2.boundingRect(cnt)

		x_left_o = max(x_o, x)
		y_top_o = max(y_o, y)
		x_right_o = min(x_o+w_o, x+w)
		y_bottom_o = min(y_o+h_o, y+h)

		x_left_i = max(x_i, x)
		y_top_i = max(y_i, y)
		x_right_i = min(x_i+w_i, x+w)
		y_bottom_i = min(y_i+h_i, y+h)

		# Filtro de tamaño
		if w < 20 or h < 10:
			continue

		# Filtro de cercania al perimetro
		if 1.1*x_right_o < x_left_o or 1.1*y_bottom_o < y_top_o:
			continue

		if x_right_i > x_left_i and y_bottom_i > y_top_i:
			continue

		# Filtro de si tienen texto
		box = cv2.resize(im[y-5:y+h+5, x-15:x+w,:], (0,0), fx=3, fy=3)
		string = pytesseract.image_to_string(box)
		if not string:
			continue

		#cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
		players.append([x-6, y, w, h])

	players = mergeCloseContours(players, im.shape[0]*im.shape[1], 9500)

	if DEBUG:
		for cnt in players:
			[x, y, w, h] = cnt
			cv2.rectangle(mock, (x, y), (x + w, y + h), (0, 0, 255), 2)
		utils.imshow(mock, 0.8)

	return players

# cnt = [x, y, w, h]
def mergeCloseContours(contours, im_area, thresh):
	other = []
	while contours:
		merged = False
		cnt1 = contours.pop()
		x1, y1, w1, h1 = cnt1
		for i, cnt2 in enumerate(contours):
			x2, y2, w2, h2 = cnt2
			near = im_area/distance.euclidean([x1+w1/2, y1+h1/2], [x2+w2/2, y2+h2/2])
			if near > thresh:
				new = utils.mergeBoxes(cnt1, cnt2)
				merged = True
				contours.pop(i)
				other.append(new)
		if not merged:
			other.append(cnt1)
	return other
