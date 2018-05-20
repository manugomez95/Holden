#!python3.6
#coding: utf8

import cv2
import numpy as np
from importlib import reload
import utils
from detectTableCards import *
import pytesseract
from scipy.spatial import distance
from operator import itemgetter
from itertools import groupby

reload(utils)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

# TODO - hacer robusto a cambios de resolucion
def findTextNearPerimeter(im, outer_perimeter, inner_perimeter, DEBUG=False):
	image_area = im.shape[0]*im.shape[1]
	[x_o, y_o, w_o, h_o] = outer_perimeter
	[x_i, y_i, w_i, h_i] = inner_perimeter

	if DEBUG: mock = im.copy()

	# Preprocessing
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
	grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, morph_kernel)
	_, bw = cv2.threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
	connected = cv2.morphologyEx(bw, cv2.MORPH_OPEN, morph_kernel, iterations=1)
	morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 3))
	connected = cv2.morphologyEx(connected, cv2.MORPH_CLOSE, morph_kernel, iterations=6)

	_, contours, hierarchy = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
	rects = [cv2.boundingRect(cnt) for cnt in contours]
	contours = []
	# filtrar por tamaño
	for r in rects:
		if r[2] < 30 or r[2] > 250 or r[3] < 10:
			continue
		contours.append(r)

	rad_distance = round(h_o*1.2/2)
	centers = [(round(x_o+0.60*w_o/2), round(y_o+h_o/2)), (round(x_o+1.4*w_o/2), round(y_o+h_o/2))]	# los dos centros de la elipse

	if DEBUG and False:
		cv2.circle(mock,centers[0], rad_distance, (0,255,0), 2)
		cv2.circle(mock,centers[1], rad_distance, (0,255,0), 2)

	th = image_area/1000
	groups, uniquekeys = groupContoursByDistance(contours, centers, th)		# grupo -> ([lista de contornos], distancia media)
	for i, group in enumerate(groups):
		if 0.5*rad_distance < uniquekeys[i] < 1.5*rad_distance and len(group)>5:
			group = groups[i]
			break
	index = [i for i,v in group]
	players =  [contours[i] for i in index]
	players = mergeCloseContours(players, im.shape[0]*im.shape[1], 9500)

	if DEBUG:
		for cnt in players:
			[x, y, w, h] = cnt
			cv2.rectangle(mock, (x-10, y-5), (x + w, y + h), (255, 100, 70), 2)
		utils.imshow(mock, 0.8)

	return players

# cnt = [x, y, w, h]
def mergeCloseContours(contours, im_area, th):
	other = []
	while contours:
		merged = False
		cnt1 = contours.pop()
		x1, y1, w1, h1 = cnt1
		for i, cnt2 in enumerate(contours):
			x2, y2, w2, h2 = cnt2
			near = im_area/distance.euclidean([x1+w1/2, y1+h1/2], [x2+w2/2, y2+h2/2])
			if near > th:
				new = utils.mergeBoxes(cnt1, cnt2)
				merged = True
				contours.pop(i)
				other.append(new)
		if not merged:
			other.append(cnt1)
	return other

# TODO - meter el im_area en un contexto global
# TODO - First time using relative distance -> im_area/(npixels*1000)
def groupContoursByDistance(rects, centers, th):
	groups = []
	uniquekeys = []
	points = [(r[0]+r[2]/2, r[1]+r[3]/2) for r in rects]
	distances = [distance.euclidean(p, nearestCenter(p, centers)) for p in points]
	enumerated = sorted(list(enumerate(distances)), key=lambda tup: tup[1])
	groups = list(grouper(enumerated, 27))
	uniquekeys = [round(np.mean([elem[1] for elem in group])) for group in groups]

	return groups, uniquekeys

def grouper(iterable, th):
    prev = None
    group = []
    for item in iterable:
        if not prev or item[1] - prev[1] <= th:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group

def nearestCenter(p, centers):
	dists = [distance.euclidean(p, center) for center in centers]
	return centers[min(enumerate(dists), key=itemgetter(1))[0]]
