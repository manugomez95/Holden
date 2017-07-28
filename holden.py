# paquetes necesarios
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from PIL import Image
from pytesseract import *

####################### FUNCIONES AUXILIARES ######################
def classify_ssim(database, names, image):
	# using ssim
    max=0
    i=0
    for example in database:
        s = ssim(image, example)
        if s>max:
            max=s
            result = names[i]
        i+=1
    return result

####################### RECONOCIMIENTO ######################
# RECONOCIMIENTO DE PALOS
# carga de los palos (suits) de referencia
suits = [0 for i in range(4)]
suits_names = ["club", "diamond", "heart", "spade"]
i=0
for suit in suits_names:
    im_name = "img/suits/" + suit + ".jpg"
    suits[i] = cv2.resize(cv2.imread(im_name, 0), (345, 431))
    i+=1

# pruebas reconocimiento de palos
diamante_prueba = cv2.resize(cv2.imread("diamante_prueba.jpg", 0), (345, 431))
corazon_prueba = cv2.resize(cv2.imread("corazon_prueba.png", 0), (345, 431))
pica_prueba = cv2.resize(cv2.imread("pica_prueba.png", 0), (345, 431))
#trebol_prueba = cv2.resize(cv2.imread("trebol_prueba.png", 0), (345, 431))

print(classify_ssim(suits, suits_names, diamante_prueba))
print(classify_ssim(suits, suits_names, corazon_prueba))
print(classify_ssim(suits, suits_names, pica_prueba))
#print(classify_ssim(suits, suits_names, trebol_prueba))

# RECONOCIMIENTO DE CARACTERES
# se obtiene la imagen de la carta
#pil_im = Image.open('')
pil_im = pil_im.convert('1', dither=Image.NONE)
pil_im = pil_im.convert('RGB')
cv_im = np.array(pil_im)
cv_im = cv_im[:, :, ::-1].copy()

# de ahi pillamos la region que nos interesa (el caracter)
c1 = 25
r1 = 0
cv_im = cv_im[c1:c1+150,r1:r1+150]

# muestra la nueva imagen
pil_im = Image.fromarray(cv_im)
pil_im.show()

# reconocimiento
text = image_to_string(pil_im, config='-psm 10')
print text

####################### PRINCIPAL ######################
# 1. Obtenemos las cartas que hay en la mesa.
# (si no hay un pixel blanco donde debería estar la carta todavía no esta puesta)
# 2. Analizamos cada carta. (funcion analizar carta?)
# 3. Concluimos estado de la mesa.
# 4. Obtenemos información valiosa (con la calculadora de probabilidades)
