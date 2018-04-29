from PIL import Image, ImageGrab
import numpy as np
import cv2
import pymouse

class Context:
	x_offset = 0
	y_offset = 0

context = Context()

def cropped_screenshot(x1,y1,x2,y2):
	screen = np.array(ImageGrab.grab())
	screen = screen[:, :, ::-1].copy()
	screen = screen[y1:y2,x1:x2,:]
	return screen

def select_window():
	mouse = pymouse.PyMouse()
	print("Change resolution to 100%")
	input("Place the cursor on the upper left corner. Press Enter to continue...")
	x1, y1 = mouse.position()
	print("Coordinates: " + str([x1,y1]))

	input("Place the cursor on the lower right corner. Press Enter to continue...")
	x2, y2 = mouse.position()
	print("Coordinates: " + str([x2,y2]))

	# Set window offset in context
	global context
	context.x_offset = x1
	context.y_offset = y1

	return x1,y1,x2,y2

def imshow(image, percentage=1):
	cv2.imshow("im", cv2.resize(image, (0,0), fx=percentage, fy=percentage))
	cv2.waitKey()
	cv2.destroyAllWindows()

def mergeBoxes(br1, br2):
	[x1, y1, w1, h1] = br1
	[x2, y2, w2, h2] = br2
	x = min(x1,x2)
	y = min(y1,y2)
	w = max(x1+w1, x2+w2)-x
	h = max(y1+h1, y2+h2)-y
	return [x, y, w, h]

# https://aspratyush.wordpress.com/2013/12/22/ginput-in-opencv-python/
def getXY(img):
	DEBUG = 0
	#define the event
	def getxy(event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			global p
			#print("(row, col) = ", (x,y))
			p = [x,y]
			cv2.destroyAllWindows()

	#Read the image
	#img = cv2.imread(imgPath)
	if (DEBUG):
		print("Reading the image...")

	#Set mouse CallBack event
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', getxy)
	if (DEBUG):
		print("Set MouseCallback functionality...")

	#show the image
	#print("Click to select a point OR press ANY KEY to continue...")
	cv2.imshow('image', img)
	cv2.waitKey(0)
	return p

def getxy():
	global context
	mouse = pymouse.PyMouse()
	input("Place the cursor and press Enter to continue...")
	x, y = mouse.position()
	return x-context.x_offset,y-context.y_offset
