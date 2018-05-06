#!python3.6
#coding: utf8

from player import Player
from importlib import reload
import card, detectTableCards, detectPlayers, detectPlayerCards, utils
reload(utils)
reload(card)
reload(detectTableCards)
reload(detectPlayers)
reload(detectPlayerCards)
from card import TableCardSet
from detectTableCards import *
from detectPlayers import *
from detectPlayerCards import *

class PokerAnalyzer:
	def __init__(self):
		self.players = None
		self.playerCards = None
		self.table = Table()
		self.context = utils.Context()

	def __str__(self):
		return str(self.table.cardSet) + str(self.playerCards)

	# Reconocimiento.
	# TODO - actualizar estado de jugadores
	def refresh(self, screen):
		self.context.t += 1
		self.table.cardSet = getTableCards(screen, self.table.cardSet)
		if self.context.player_cards_flag:
			self.playerCards = getPlayerCards(screen, self.playerCards)

	# Detección
	def initialScan(self, screen, VERBOSE=False):	# Se puede mejorar calculando resultados en paralelo.
		self.context.t += 1
		if not self.table.cardSet.verified:	# tenemos las cartas de la mesa?
			self.table.cardSet = getTableCards(screen, self.table.cardSet)
		else:
			#self.table.cardSet = getTableCards(screen, self.table.cardSet)	# TODO - queda bien en la foto, pero no hace falta
			if self.table.cardSet.white_tone is None:	# vale, tenemos las cartas de la mesa... tenemos el blanco?
				self.table.cardSet.white_tone = getWhite(screen, self.table.cardSet)
			elif self.playerCards is None and self.context.player_cards_flag:
				player_loc = utils.getxy()
				# TODO - pasarle como argumento a estas funciones self, para tener el contexto
				self.playerCards = detectPlayerCards(screen, self.table.cardSet.white_tone, player_loc)

			if self.table.outer_perimeter is None:	# tenemos la mesa?
				self.detectTable(screen)
			elif self.players is None: # vale, tenemos la mesa, tenemos jugadores? No
				self.detectPlayers(screen)

		# return False # cuando acabe
		self.updateStatus(self.context.player_cards_flag)
		if self.context.status == "Initial scan completed.":
			return False
		else:
			return True

	# localiza a los jugadores
	def detectPlayers(self, image, DEBUG=False):
		self.players = findTextNearPerimeter(image, self.table.outer_perimeter, self.table.inner_perimeter, DEBUG)

	# necesita las TableCards verificadas
	def detectTable(self, im, DEBUG=False):
		self.table.color = np.array(getTableColor(im, self.table.cardSet))
		COLOR_RANGE = [self.table.color-self.table.color*0.6,self.table.color+self.table.color*0.9]
		color_mask = cv2.inRange(im, COLOR_RANGE[0], COLOR_RANGE[1])

		_, contours, hierarchy = cv2.findContours(color_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnt = sorted(contours, key = cv2.contourArea, reverse = True)[0]
		[x_o, y_o, w_o, h_o] = cv2.boundingRect(cnt)

		self.table.outer_perimeter = [x_o, y_o, w_o, h_o]
		[x_i, y_i, w_i, h_i] = [x_o+0.15*w_o, y_o+0.25*h_o, w_o*0.7, h_o*0.5]
		self.table.inner_perimeter = [x_i, y_i, w_i, h_i]

		if DEBUG:
			mock = im.copy()
			# utils.imshow(color_mask, 0.8)
			cv2.rectangle(mock, (int(x_o), int(y_o)), (int(x_o) + int(w_o), int(y_o) + int(h_o)), (0, 255, 0), 2)
			cv2.rectangle(mock, (int(x_i), int(y_i)), (int(x_i) + int(w_i), int(y_i) + int(h_i)), (0, 255, 0), 2)
			utils.imshow(mock, 0.8)
		return

	def show(self, image):
		# posicion de las cartas
		self.table.cardSet.draw(image)

		# posicion de la mesa
		[x, y, w, h] = self.table.outer_perimeter
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# posicion de los jugadores
		if self.players:
			for cnt in self.players:
				[x, y, w, h] = cnt
				cv2.rectangle(image, (x-10, y-5), (x + w, y + h), (255, 100, 70), 2)

		if self.playerCards:
			self.playerCards.draw(image)

		utils.imshow(image, 0.8)
		#cv2.imwrite("../mesa.png", image)

	def updateStatus(self, player_cards_flag):
		conditions = []
		conditions.append(self.table.cardSet.white_tone)
		conditions.append(self.table.outer_perimeter)
		conditions.append(self.players)
		if player_cards_flag:
			conditions.append(self.playerCards)
		if all(conditions):
			self.context.status = "Initial scan completed."
