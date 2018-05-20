#!python3.6
#coding: utf8

import time, os
import utils, detectTableCards, pokerAnalyzer
from importlib import reload
reload(pokerAnalyzer)
reload(utils)
from pokerAnalyzer import PokerAnalyzer

refresh_rate = 1

analyzer = PokerAnalyzer()
analyzer.context.player_cards_flag = True
x1,y1,x2,y2 = utils.select_window()
os.system('cls')

# Primero scan inicial para obtener todas las ubicaciones posibles
while analyzer.initialScan(utils.cropped_screenshot(x1,y1,x2,y2)):
	pass

# Segundo bucle más eficiente
while True:
	screen = utils.cropped_screenshot(x1,y1,x2,y2)
	analyzer.refresh(screen)
	os.system('cls')
	print(analyzer)

	time.sleep(refresh_rate)
