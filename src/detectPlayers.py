import cv2
import numpy as np
from importlib import reload
import utils
from detectTableCards import *
import pytesseract
from scipy.spatial import distance

reload(utils)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def findTextNearPerimeter(im, outer_perimeter, inner_perimeter):
	[x_o, y_o, w_o, h_o] = outer_perimeter
	[x_i, y_i, w_i, h_i] = inner_perimeter

	# apply grayscale
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	# morphological gradient
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))	# MUY INTERESANTE
	grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, morph_kernel)
	#utils.imshow(grad, 0.7)
	# binarize
	#_, bw = threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
	_, bw = cv2.threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))	# 4, 8?
	# connect horizontally oriented regions
	connected = cv2.morphologyEx(bw, cv2.MORPH_OPEN, morph_kernel, iterations=1)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 3))
	connected = cv2.morphologyEx(connected, cv2.MORPH_CLOSE, morph_kernel, iterations=6)
	mask = np.zeros(bw.shape, np.uint8)
	# find contours
	im2, contours, hierarchy = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
		if w < 5 or h < 5:
			continue

		# Filtro de cercania al perimetro
		if 1.1*x_right_o < x_left_o or 1.1*y_bottom_o < y_top_o:
			continue

		if x_right_i > x_left_i and y_bottom_i > y_top_i:
			continue

		# Filtro de si tienen texto
		box = im[y-10:y+h+5, x-10:x+w+5,:]
		string = pytesseract.image_to_string(box)
		if not string:
			continue

		#cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
		players.append([x, y, w, h])

	players = mergeCloseContours(players, im.shape[0]*im.shape[1], 9000)
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

def findPatternsNearPerimeter(im, outer_perimeter, inner_perimeter):
	[x_o, y_o, w_o, h_o] = outer_perimeter
	[x_i, y_i, w_i, h_i] = inner_perimeter

	img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	x1,y1,x2,y2 = utils.select_window()
	template = cv2.cvtColor(utils.cropped_screenshot(x1,y1,x2,y2), cv2.COLOR_BGR2GRAY)
	utils.imshow(template, 1)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.35
	loc = np.where(res >= threshold)
	for pt in zip(*loc[::-1]):
		x = pt[0]
		y = pt[1]

		x_left_o = max(x_o, x)
		y_top_o = max(y_o, y)
		x_right_o = min(x_o+w_o, x+w)
		y_bottom_o = min(y_o+h_o, y+h)

		x_left_i = max(x_i, x)
		y_top_i = max(y_i, y)
		x_right_i = min(x_i+w_i, x+w)
		y_bottom_i = min(y_i+h_i, y+h)

		if 1.1*x_right_o < x_left_o or 1.1*y_bottom_o < y_top_o:
			continue

		if x_right_i > x_left_i and y_bottom_i > y_top_i:
			continue

		cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

	utils.imshow(im, 0.7)


# for i in range(4):
# 	image = cv2.imread('../img/mesas/mesa'+str(i+1)+'.png')
# 	cardSet = getTableCards(image, None)
# 	cardSet = getTableCards(image, cardSet)
# 	color = np.array(getTableColor(image, cardSet))
# 	COLOR_RANGE = [color-color*0.55,color+color*0.55]
# 	color_mask = cv2.inRange(image, COLOR_RANGE[0], COLOR_RANGE[1])
#
# 	_, contours, hierarchy = cv2.findContours(color_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#
# 	for contour in contours:
# 		[x, y, w, h] = cv2.boundingRect(contour)
# 		if w < 400 or h < 100:
# 			continue
#
# 		br = [x, y, w, h]
# 		[x_i, y_i, w_i, h_i] = [round(x+0.25*w), round(y+0.25*h), round(w*0.5), round(h*0.5)]		#inner perimeter
#
# 	findTextNearPerimeter(image, br, [x_i, y_i, w_i, h_i])
