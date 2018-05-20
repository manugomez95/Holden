#!python3.6
#coding: utf8

from PIL import ImageGrab
import numpy as np
import cv2
import pymouse

# almacena variables contextuales útiles para pokerAnalyzer
class Context:
	def __init__(self):
		self.t = 0
		self.x_offset = 0
		self.y_offset = 0
		self.image_area = 0
		self.status = "Initial scan in process..."
		self.player_cards_flag = False

context = Context()

# output: las coordenadas de un marco seleccionado por el usuario
def select_window():
	mouse = pymouse.PyMouse()
	print("Selecting frame...")
	input("Place the cursor on the upper left corner. Press Enter to continue...")
	x1, y1 = mouse.position()

	input("Place the cursor on the lower right corner. Press Enter to continue...")
	x2, y2 = mouse.position()

	if x2 < x1 or y2 < y1:
		print("\nThe input is incorrect. Try again.\n\n")
		return select_window()

	# Set window offset in context
	global context
	context.x_offset = x1
	context.y_offset = y1

	return x1,y1,x2,y2

# output: captura de pantalla recortada
def cropped_screenshot(x1,y1,x2,y2):
	screen = np.array(ImageGrab.grab())
	screen = screen[:, :, ::-1].copy()
	screen = screen[y1:y2,x1:x2,:]
	return screen

# output: devuelve coordenadas relativas al frame seleccionado previamente
def getxy():
	global context
	mouse = pymouse.PyMouse()
	input("Place the cursor and press Enter to continue...")
	x, y = mouse.position()
	return x-context.x_offset,y-context.y_offset

def imshow(image, percentage=1):
	cv2.imshow("im", cv2.resize(image, (0,0), fx=percentage, fy=percentage))
	cv2.waitKey()
	cv2.destroyAllWindows()

# input: dos bounding rect [x, y, w, h]
# ouput: union de los dos br
def mergeBoxes(br1, br2):
	[x1, y1, w1, h1] = br1
	[x2, y2, w2, h2] = br2
	x = min(x1,x2)
	y = min(y1,y2)
	w = max(x1+w1, x2+w2)-x
	h = max(y1+h1, y2+h2)-y
	return [x, y, w, h]
