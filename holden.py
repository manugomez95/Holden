from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from PIL import Image
from pytesseract import *

# globales
# IMPORTANTE! VALORES CONCRETOS PARA CARTAS EN ZYNGA
# posible mejora: hacerlo mas general
c1=10; r1=15; c2=c1+145; r2=25

####################### FUNCIONES AUXILIARES ######################
# input:	database, las imagenes de los palos de referencia
#			names, los nombres de cada palo
#			image, imagen del palo que se quiere clasificar
# output:	"club", "diamond", "heart" o "spade"
def classify_ssim(database, names, image):
	# usando ssim
    max=0
    i=0
    for example in database:
        s = ssim(image, example)
        print(names[i] + ' = ' + str(s))
        if s>max:
            max=s
            result = names[i]
        i+=1
    return result

# input:	carta, imagen de la carta completa
# output:	valor en formato string del 2 al 10, A, J, Q o K
def carta_valor(carta):
    valor_cv = carta[c1:c1+150,r1:r1+145]
    valor_pil = Image.fromarray(valor_cv)
	# aqui ocurre la magia, esta funcion es de pytesseract
    valor = image_to_string(valor_pil, config='-psm 10')
    # CHAPUZA -> 10 lo detecta como m
    if valor == 'm':
        valor = '10'
    return valor

# input:	carta, imagen de la carta completa
# output:	"club", "diamond", "heart" o "spade"
def carta_palo(carta):
    palo_cv = cv2.resize(carta[c2:c2+145,r2:r2+115], (345, 431))
    palo = classify_ssim(suits, suits_names, palo_cv)
    return palo

# input:	carta, imagen de la carta completa
# output:	nombre de la carta listo para pasarlo a holdem_calc
def reconocer_carta(carta):
    return carta_valor(carta)+carta_palo(carta)[0]

##################################################################
# carga de los palos (suits) de referencia globales
suits = [0 for i in range(4)]
suits_names = ["club", "diamond", "heart", "spade"]
i=0
for suit in suits_names:
    im_name = "img/suits/" + suit + ".png"
    suits[i] = cv2.resize(cv2.imread(im_name, 0), (345, 431))
    i+=1
##################################################################

################## CODIGO QUE SE EJECUTA #########################

# obtenemos imagen de una carta y la reconocemos
carta = cv2.resize(cv2.imread('img/pruebas/carta5.png', 0), (345, 431))
print(reconocer_carta(carta))
