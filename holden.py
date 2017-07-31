# paquetes necesarios
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from PIL import Image
from pytesseract import *

# globales
# IMPORTANTE! VALORES CONCRETOS PARA CARTAS EN ZYNGA
c1=10; r1=15; c2=c1+145; r2=25

####################### FUNCIONES AUXILIARES ######################
def classify_ssim(database, names, image):
	# using ssim
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

def carta_valor(carta):
    valor_cv = carta[c1:c1+150,r1:r1+145]
    valor_pil = Image.fromarray(valor_cv)
    valor = image_to_string(valor_pil, config='-psm 10')
    # CHAPUZA -> 10 lo detecta como m
    if valor == 'm':
        valor = '10'
    return valor

def carta_palo(carta):
    palo_cv = cv2.resize(carta[c2:c2+145,r2:r2+115], (345, 431))
    palo = classify_ssim(suits, suits_names, palo_cv)
    return palo

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

# obtenemos imagen de una carta y la reconocemos
carta = cv2.resize(cv2.imread('img/pruebas/carta6.png', 0), (345, 431))
print(reconocer_carta(carta))

####################### PRINCIPAL ######################
# 1. Obtenemos las cartas que hay en la mesa.
# (si no hay un pixel blanco donde deberia estar la carta todavia no esta puesta)
# 2. Analizamos cada carta. (funcion analizar carta?)
# 3. Concluimos estado de la mesa.
# 4. Obtenemos informacion valiosa (con la calculadora de probabilidades)

################ MEJORAS PENDIENTES ####################
# 1. Adaptacion sencilla a un nuevo tipo de baraja:
#   - Le pasas una captura de una carta de cada palo (de la nueva baraja)
#     indicandole las regiones importantes. El sistema aprende a reconocer los
#     nuevos palos incluyendo capturas de ellos en img/suits
# 2. Identificar cuantos jugadores hay en la mesa.
# 3. Automatizar obtencion de c1, c2, r1 y r2 y posicion de todo en general.

# DIMENSIONES DE LAS CARTAS: 49x36
# ESPACIO ENTRE LAS CARTAS: 3-4 pixeles
# PUNTO DE REFERENCIA: x:432, y:398-399
