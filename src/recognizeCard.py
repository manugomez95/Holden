#!python3.6
#coding: utf8

from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from PIL import Image
import utils
import pytesseract
from card import *
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

# input:	carta, imagen de la carta completa
# output:	lista de tuplas (valor, palo)
def identifyCards(image, DEBUG=False):
	COLOR_RANGE = [175, 255]	# TODO pendiente de revisar
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	color_mask = cv2.inRange(gray, COLOR_RANGE[0], COLOR_RANGE[1])
	m = np.mean(color_mask)
	if m < 100:
		return None

	_, contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cards = []
	while contours:
		contour1 = contours.pop()
		[x1, y1, w1, h1] = cv2.boundingRect(contour1)
		if 10 < w1 and 15 < h1:
			for contour2 in contours:
				[x2, y2, w2, h2] = cv2.boundingRect(contour2)
				if 10 < w2 and 15 < h2:
					similar_x = x1-x1*0.7 < x2 < x1+x1*0.7
					similar_w = w1-w1*1.3 < w2 < w1+w1*1.3
					similar_h = h1-h1*0.5 < h2 < h1+h1*0.5
					y_condition = y1+h1 <= y2 < y1+1.5*h1
					if all([similar_x, similar_w, similar_h, y_condition]):
						value_im = cv2.resize(color_mask[y1:y1+h1, x1:x1+w1],(0,0), fx=4, fy=4)
						value = obtain_value(value_im)

						suit_im = image[y2:y2+h2, x2:x2+w2,:]
						suit = obtain_suit(suit_im, contour2)

						if DEBUG:
							cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 255), 1)
							cv2.rectangle(image, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 255), 2)

						cards.append((value, suit))

	if DEBUG:
		utils.imshow(image, 2)
		print(cards)

	return cards

# input:	carta, imagen de la carta completa
# output:	valor en formato string del 2 al 10, A, J, Q o K
def obtain_value(value_im):
	value_im = cv2.medianBlur(value_im, 3)
	return pytesseract.image_to_string(value_im, config="--psm 10")

# input:	carta, imagen de la carta completa
# output:	"club", "diamond", "heart" o "spade"
def obtain_suit(suit_im, contour):
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.025 * peri, True)
	if len(approx) == 4 and np.mean(suit_im[:,:,2], axis=None) > 170:
		return Suits.DIAMONDS
	elif 5 <= len(approx) <= 8 and np.mean(suit_im[:,:,2], axis=None) > 170:
		return Suits.HEARTS
	elif len(approx) <= 10 and np.mean(suit_im[:,:,2], axis=None) < 170:
			return Suits.SPADES
	elif np.mean(suit_im[:,:,2], axis=None) < 170:
		return Suits.CLUBS
	else:
		return None