#!python3.6
#coding: utf8

from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
from scipy import stats

class Suits(Enum):
	HEARTS = "♥"
	DIAMONDS = "♦"
	CLUBS = "♣"
	SPADES = "♠"
	
	def __str__(self):
		return self.value

class Card:
	value = None
	suit = None
	vertexes = []	# 2 o 4? 2 de momento
	
	def __init__(self, value, suit, vertexes):
		self.value = value
		self.suit = suit
		self.vertexes = vertexes
	
	def __str__(self):
		return (str(self.value) + str(self.suit)).replace(str(None), "?")
		
	def __eq__(self, other):
		if self.value == other.value and self.suit == other.suit:
			return True
		else:
			return False
			
	def size(self):
		height = self.vertexes[1][1] - self.vertexes[0][1]
		width = self.vertexes[1][0] - self.vertexes[0][0]
		return [height, width]

class CardSet(ABC):
	name = None
	cards = []
	verified = False
	def __init__(self, cards):
		cards.sort(key=lambda x: x.vertexes[0][0])
		self.cards = cards
		self.verified = self.verify()
	
	# Incluir proximamente, si no está verificado: "Calibrating..."
	def __str__(self):
		if self.verified:
			return self.name + ': [' + ', '.join(str(c) for c in self.cards) + ']'
		else:
			return self.name + ': Verifying...'

	@abstractmethod
	def verify(self):
		pass
		
	def add(self, card):
		self.cards.append(card)
		self.cards.sort(key=lambda x: x.vertexes[0][0])
		return self
	
class PlayerCardSet(CardSet):
	name = "Player Cards"
	
	def verify(self):
		pass
		
class TableCardSet(CardSet):
	name = "Table Cards"
	white_tone = None	# Tengo que sacar esto
	height_mode = None
	weight_mode = None
	distance_mode = None
	x = []
	y = None

	# verifica que se han encontrado las cartas y produce datos utiles para las fases siguientes
	def verify(self):
		if len(self.cards) >= 3:
			heights = [x.size()[0] for x in self.cards]
			widths = [x.size()[1] for x in self.cards]
			distances = [self.cards[i+1].vertexes[0][0]-self.cards[i].vertexes[0][0] for i in range(len(self.cards)-1)]
			
			self.height_mode = int(stats.mode(heights)[0])
			self.width_mode = int(stats.mode(widths)[0])
			self.distance_mode = int(stats.mode(distances)[0])
			
			self.x = [c.vertexes[0][0] for c in self.cards]
			self.y = int(stats.mode([c.vertexes[0][1] for c in self.cards])[0])
			
			height_verified = np.std(heights) < 4
			width_verified = np.std(widths) < 4
			axis_verified = np.std(self.y) < 4
			return all([height_verified, width_verified, axis_verified])
		return False
		
	def add(self, card):
		self.cards.append(card)
		self.cards.sort(key=lambda x: x.vertexes[0][0])
		diff = abs(card.vertexes[0][0] - np.array(self.x))
		if any(diff < 5):
			return self
		self.x.append(card.vertexes[0][0])
		self.x.sort()
		return self