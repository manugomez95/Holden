import numpy as np
import cv2
from importlib import reload
import utils, card, recognizeCard
reload(utils)
reload(card)
reload(recognizeCard)
from card import Card, TableCardSet
from recognizeCard import *
import copy
from scipy import stats

class Table:
	cardSet = None
	color = None
	inner_perimeter = None
	outer_perimeter = None

	def __init__(self):
		self.cardSet = TableCardSet([])

# Devuelve un TableCardSet
def locateTableCards(image, DEBUG=False):
	cv2.imwrite("../cuarentena.png", image)
	image_area = image.shape[0]*image.shape[1]	# TODO - uso el area
	if DEBUG: mock = image.copy()

	# rango de blancos
	COLOR_RANGE = [180, 255]	# TODO - rangos
	# rango de ratios altura/anchura
	RATIO_RANGE = [1.3, 1.7]
	# rango de areas
	AREA_RANGE = [image_area/500, image_area/50]

	# aplicamos máscara de luminosidad
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	color_mask = cv2.inRange(gray, COLOR_RANGE[0], COLOR_RANGE[1])

	# búsqueda de contornos
	_, cnts, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# cnts guarda los 20 contornos con el mayor area
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]

	cards = []

	# para cada contorno
	for c in cnts:
		# se aproxima el contorno
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.05 * peri, True)
		# primer filtro: cuatro lados?
		if len(approx) == 4:
			[x, y, w, h] = cv2.boundingRect(c)
			if w != 0: ratio = h/w
			else: continue
			area = h*w
			# segundo filtro: forma de carta?
			ratio_verified = RATIO_RANGE[0]<ratio<RATIO_RANGE[1]
			area_verified = AREA_RANGE[0]<area<AREA_RANGE[1]
			if all([ratio_verified, area_verified]):
				cards.append(Card(None, None,[(x,y), (x+w,y+h)]))
				if DEBUG:
					cv2.rectangle(mock, (x, y), (x + w, y + h), (0, 255, 0), 2)

	if DEBUG:
		utils.imshow(mock, 0.70)

	return TableCardSet(cards)

def look(direction, image, cardSet, x1):
	x2 = x1+cardSet.width_mode
	if direction == -1:
		new_x1 = x1 - cardSet.distance_mode
	elif direction == 1:
		new_x1 = x1 + cardSet.distance_mode
	elif direction == 0:
		new_x1 = x1
	else:
		raise Exception("detectTableCards/look argument error")

	new_x2 = new_x1+cardSet.width_mode
	y1 = cardSet.y
	y2 = y1+cardSet.height_mode

	card_im = image[y1-10:y2+10, new_x1-10:new_x2+10]

	ret = identifyCards(card_im)	# lista de tuplas valor, palo
	if ret:
		value, suit = ret[0]
		card = Card(value, suit, [[new_x1, y1],[new_x2, y2]])
		if direction == 0:
			return cardSet.add(card)
		else:
			return look(direction, image, cardSet.add(card), new_x1)
	else:
		return cardSet

def getTableCards(image, cardSet, DEBUG=False):
	if cardSet is None or not cardSet.verified:
		if DEBUG: print("Cards not verified: Locating...")
		return locateTableCards(image, DEBUG)	# ¿QUE DEVUELVA TAMBIEN UN ESTADO?	TODO
	else:
		if DEBUG: print("Cards verified: Completing and updating value")
		# resetear cartas
		new_cardSet = copy.deepcopy(cardSet)
		new_cardSet.cards = []
		new_cardSet = look(0, image, new_cardSet, cardSet.x[0])		# ¿La primera carta que detectaste antes, sigue ahí?
		new_cardSet = look(-1, image, new_cardSet, cardSet.x[0])	# Mira a tu izquierda
		new_cardSet = look(1, image, new_cardSet, cardSet.x[0])		# Y a tu derecha
		return new_cardSet

def getWhite(image, cardSet):
	COLOR_RANGE = [150, 255]	# Color de una carta
	x1 = cardSet.x[0]
	y1 = cardSet.y
	x2 = x2 = x1+cardSet.width_mode
	y2 = y1+cardSet.height_mode
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	color_mask = cv2.inRange(gray, COLOR_RANGE[0], COLOR_RANGE[1])
	masked_im = cv2.bitwise_and(gray, gray, mask=color_mask)
	card = masked_im[y1:y2, x1:x2]
	color = np.median(card[card > COLOR_RANGE[0]])
	return color

def getTableColor(image, cardSet):
	COLOR_RANGE = [150, 255]	# Color de una carta
	x1 = cardSet.x[0]-cardSet.width_mode
	y1 = cardSet.y-cardSet.width_mode
	x2 = cardSet.x[0]+2*cardSet.width_mode
	y2 = cardSet.y

	table_sample = image[y1:y2, x1:x2, :]
	b = int(stats.mode(table_sample[:,:,0], axis=None)[0])
	g = int(stats.mode(table_sample[:,:,1], axis=None)[0])
	r = int(stats.mode(table_sample[:,:,2], axis=None)[0])
	return [b,g,r]
