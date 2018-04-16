import sys
sys.path.insert(0, r'C:\Users\manue\Documents\TFG\Holden\src')
import cv2
import numpy as np
import utils
import pytesseract
import recognizeCard
from importlib import reload
reload(recognizeCard)
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

# RECONOCIMIENTO DE CARTAS SOLAPADAS // SUFICIENTE... PERO PENDIENTE DE MEJORAR

for i in range(0,4):
	img_rgb = cv2.imread('../img/cartasJugador/mesa'+str(i+1)+'.png')
	print(recognizeCard.identifyCards(img_rgb))
	print("--------------------")