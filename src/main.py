import time, os
import utils, detectTableCards, pokerAnalyzer
from importlib import reload
reload(pokerAnalyzer)
reload(utils)
from pokerAnalyzer import PokerAnalyzer

refresh_rate = 3

analyzer = PokerAnalyzer()
x1,y1,x2,y2 = utils.select_window()
os.system('cls')

# Primero scan inicial para obtener todas las ubicaciones posibles
while analyzer.initialScan(utils.cropped_screenshot(x1,y1,x2,y2)):
	pass
	#time.sleep(refresh_rate)

# Show location of each
analyzer.show(utils.cropped_screenshot(x1,y1,x2,y2))

# Segundo bucle más eficiente
# while True:
	# screen = utils.cropped_screenshot(x1,y1,x2,y2)
	# os.system('cls')

	# analyzer.refresh(screen)
	# print(analyzer)

	# time.sleep(refresh_rate)
