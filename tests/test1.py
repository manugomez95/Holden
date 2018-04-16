#!python3.6
#coding: utf8

# PROMETE PARA ENCONTRAR LAS CARTAS DE JUGADOR, Y BUEN SUSTITUO A ENCONTRAR CARTAS EN GENERAL (SOBRETODO ESTO)

import sys
sys.path.insert(0, r'C:\Users\manue\Documents\TFG\Holden\src')

import utils
import cv2

def captch_ex(file_name):
	img = cv2.imread(file_name)

	img_final = cv2.imread(file_name)
	img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)	# cuidao, esto es para cartas
	image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
	ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv2.THRESH_BINARY_INV
	# th3 = cv2.adaptiveThreshold(image_final,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
	'''
			line  8 to 12  : Remove noisy portion 
	'''
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated = cv2.dilate(new_img, kernel, iterations=13)  # dilate , more the iteration more the dilation #9 funciona bien
	# for cv2.x.x
	# Otsu's thresholding after Gaussian filtering
	blur = cv2.GaussianBlur(image_final,(5,5),0)
	ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	utils.imshow(th3, 1)

	image, contours, hierarchy = cv2.findContours(th3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:
		# get rectangle bounding contour
		[x, y, w, h] = cv2.boundingRect(contour)
		# Don't plot small false positives that aren't text
		if (w < 35 and h < 35) or (w > 500 and h > 500):
			continue

		# draw rectangle around contour on original image
		cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

		'''
		#you can crop image and send to OCR  , false detected will return no text :)
		cropped = img_final[y :y +  h , x : x + w]

		s = file_name + '/crop_' + str(index) + '.jpg' 
		cv2.imwrite(s , cropped)
		index = index + 1

        '''
	# write original image with added contours to disk
	utils.imshow(img, 1)


for i in range(0,5):
	file_name = '../img/mesas/mesa'+str(i+1)+'.png'
	captch_ex(file_name)


# MEJORAR CALIDAD DE TEXTO
	
# from PIL import Image, ImageEnhance, ImageFilter

# im = Image.open('img/pruebas/mesa1.png') # the second one 
# im.show()
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
# im.save('temp2.jpg')
# text = pytesseract.image_to_string(Image.open('temp2.jpg'))
# print(text)