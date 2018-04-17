from player import Player
from importlib import reload
import card, detectTableCards, detectPlayers, detectPlayerCards
reload(card)
reload(detectTableCards)
reload(detectPlayers)
reload(detectPlayerCards)
from card import TableCardSet
from detectTableCards import *
from detectPlayers import *
from detectPlayerCards import *

class PokerAnalyzer:
	# PLAYERS
	players = None	# Array de player.Player
	playerCards = None
	# TABLE		# crear objeto table?
	table = Table()

	# def __init__(self):
		# myPlayer = MyPlayer()
		# self.table = Table()

	def __str__(self):
		return str(self.table.cardSet)

	# actualiza el estado de los elementos ya localizados: computacionalmente ligero
	def refresh(self, screen):

		# Detectar zona de chat y tablero

		# Detectar cartas
		self.tableCards = getTableCards(screen, self.table.cardSet)	# Devuelve también un estado
		# if self.tableCards.verified:
			# playerCards = getPlayerCards(screen, )
		# si el estado dice que hay que analizar una carta se analiza... Tenemos screen, y tenemos la posicion de una carta

	# localiza todos los elementos: computacionalmente pesado
	def initialScan(self, screen):	# Se puede mejorar calculando resultados en paralelo.
		if not self.table.cardSet.verified:	# tenemos las cartas de la mesa?
			self.table.cardSet = getTableCards(screen, self.table.cardSet)
		else:
			self.table.cardSet = getTableCards(screen, self.table.cardSet)	# TODO - queda bien en la foto, pero no hace falta
			if self.table.cardSet.white_tone is None:	# vale, tenemos las cartas de la mesa... tenemos el blanco?
				self.table.cardSet.white_tone = getWhite(screen, self.table.cardSet)

			if self.table.outer_perimeter is None:	# tenemos la mesa?
				self.detectTable(screen)
			elif self.players is None: # vale, tenemos la mesa, tenemos jugadores y su detalle? No
				self.detectPlayers(screen)
				# if :# tenemos jugadores?
					# detectar jugadores
				# else :
					# detectar detalle

			elif self.table.cardSet.white_tone: # vale, tenemos a los jugadores, tenemos el color de las cartas?
				player_loc = utils.getxy()
				self.playerCards = detectPlayerCards(screen, self.table.cardSet.white_tone, player_loc)
				return False

		# return False # cuando acabe
		return True

	# localiza a los jugadores
	def detectPlayers(self, image, DEBUG=False):
		self.players = findTextNearPerimeter(image, self.table.outer_perimeter, self.table.inner_perimeter, DEBUG)

	# necesita las TableCards verificadas
	def detectTable(self, im, DEBUG=False):
		self.table.color = np.array(getTableColor(im, self.table.cardSet))
		COLOR_RANGE = [self.table.color-self.table.color*0.55,self.table.color+self.table.color*0.9]
		color_mask = cv2.inRange(im, COLOR_RANGE[0], COLOR_RANGE[1])
		if DEBUG:
			mock = im.copy()
			utils.imshow(color_mask, 0.8)

		_, contours, hierarchy = cv2.findContours(color_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnt = sorted(contours, key = cv2.contourArea, reverse = True)[0]
		[x_o, y_o, w_o, h_o] = cv2.boundingRect(cnt)

		self.table.outer_perimeter = [x_o, y_o, w_o, h_o]
		[x_i, y_i, w_i, h_i] = [x_o+0.15*w_o, y_o+0.25*h_o, w_o*0.7, h_o*0.5]
		self.table.inner_perimeter = [x_i, y_i, w_i, h_i]

		if DEBUG:
			cv2.rectangle(mock, (int(x_o), int(y_o)), (int(x_o) + int(w_o), int(y_o) + int(h_o)), (0, 255, 0), 2)
			cv2.rectangle(mock, (int(x_i), int(y_i)), (int(x_i) + int(w_i), int(y_i) + int(h_i)), (0, 255, 0), 2)
			utils.imshow(mock, 0.8)
		return

	def show(self, image):
		# posicion de las cartas
		y = self.table.cardSet.y
		w = self.table.cardSet.width_mode
		h = self.table.cardSet.height_mode
		for i, card in enumerate(self.table.cardSet.cards):
			cv2.rectangle(image, (self.table.cardSet.x[i], y), (self.table.cardSet.x[i] + w, y + h), (255, 0, 0), 2)

		# posicion de la mesa
		[x, y, w, h] = self.table.outer_perimeter
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# posicion de los jugadores
		for cnt in self.players:
			[x, y, w, h] = cnt
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

		for card in self.playerCards:
			cv2.rectangle(image, tuple(card.vertexes[0]), tuple(card.vertexes[1]), (255, 150, 20), 2)

		utils.imshow(image, 0.8)
		#cv2.imwrite("../mesa.png", image)
