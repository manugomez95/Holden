#!python3.6
#coding: utf8

import cv2
import sys
from importlib import reload
from scipy.spatial import distance

import utils, card, recognizeCard
reload(utils)
reload(card)
reload(recognizeCard)
from card import Card, PlayerCardSet
from recognizeCard import identifyCards

# para cuando las cartas están pegadas
def getPlayerCards(image, cardSet):
	cardSet.cards = []
	[x, y, w, h] = cardSet.frame
	card_im = image[y:y+h, x:x+w]
	ret = identifyCards(card_im)	# lista de tuplas valor, palo
	if len(ret) >= 2:
		value, suit = ret[0]
		cardSet.add(Card(value, suit, [[x, y],[int(x+w/2.4), y+h]]))
		value, suit = ret[1]
		cardSet.add(Card(value, suit, [[int(x+w/2.4), y],[x+w, y+h]]))
	return cardSet


def detectPlayerCards(image, white, player_loc, DEBUG=False):
	ONE_RATIO_RANGE = [1.3, 1.7]
	TWO_RATIO_RANGE = [0.65, 0.85]
	WHITE_RANGE = [white-white*0.15,white+white*0.15]
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	color_mask = cv2.inRange(gray, WHITE_RANGE[0], WHITE_RANGE[1])
	new_img = cv2.bitwise_and(gray, gray, mask=color_mask)

	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated = cv2.dilate(new_img, kernel, iterations=13)  # dilate , more the iteration more the dilation #9 funciona bien
	# for cv2.x.x
	# Otsu's thresholding after Gaussian filtering
	blur = cv2.GaussianBlur(new_img,(5,5),0)
	ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#utils.imshow(th3, 1)

	if DEBUG: utils.imshow(th3, 1)

	_, contours, hierarchy = cv2.findContours(th3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cards = PlayerCardSet([])
	for contour in contours:
		# get rectangle bounding contour
		[x, y, w, h] = cv2.boundingRect(contour)
		# Don't plot small false positives that aren't text
		if w != 0:
			ratio = h/w
		ratio_one = ONE_RATIO_RANGE[0]<ratio<ONE_RATIO_RANGE[1]
		ratio_two = TWO_RATIO_RANGE[0]<ratio<TWO_RATIO_RANGE[1]

		if (w < 35 and h < 35) or (w > 500 and h > 500):
			continue

		if not ratio_one and not ratio_two:
			continue

		max_near = 6000
		near = image.shape[0]*image.shape[1]/distance.euclidean(player_loc, [x, y])
		if near < max_near:
			continue

		# meter más filtros, de color, de cercania al input, etc...
		card_im = image[y:y+h, x:x+w]
		ret = identifyCards(card_im)	# lista de tuplas valor, palo
		if ret and ratio_one:	# de momento no me he encontrado ningún caso # Restriccion - cartas pegadas
			value, suit = ret[0]
			cards.add(Card(value, suit, [[x, y],[x+w, y+h]]))
		elif ret and ratio_two:
			value, suit = ret[0]
			cards.add(Card(value, suit, [[x, y],[int(x+w/2.4), y+h]]))
			value, suit = ret[1]
			cards.add(Card(value, suit, [[int(x+w/2.4), y],[x+w, y+h]]))
			cards.frame = [x, y, w, h]
		else:
			continue

		# draw rectangle around contour on original image
		# cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)

	# write original image with added contours to disk
	# print(', '.join(str(c) for c in cards))
	# utils.imshow(image, 0.7)
	return cards
