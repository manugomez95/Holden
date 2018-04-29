import unittest
import sys, cv2
from importlib import reload

sys.path.insert(0, r'C:\Users\manue\Documents\TFG\Holden\src')

import recognizeCard, detectTableCards, pokerAnalyzer
reload(recognizeCard)
reload(detectTableCards)
reload(pokerAnalyzer)
from recognizeCard import identifyCards
from detectTableCards import getTableCards
from pokerAnalyzer import *

class RecognizeCardsTests(unittest.TestCase):

    # def test_recognize_individual_cards(self):
    #     ncards = [5, 4, 5, 5, 4]
    #     for i in range(5):
    #         im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
    #         card_set = getTableCards(im, None, DEBUG=False)
    #         card_set = getTableCards(im, card_set, DEBUG=True)
    #         self.assertEqual(len(card_set.cards), ncards[i])

    def test_recognize_individual_cards(self):
        im = cv2.imread('../img/fails/table3.png')
        card_set = getTableCards(im, None, DEBUG=False)
        card_set = getTableCards(im, card_set, DEBUG=True)

    #
    # # TODO - Comprobar contenido y orden
    # def test_recognize_player_cards(self):
    #     for i in range(4):
    #         im = cv2.imread('../img/playerCards/cardSet'+str(i+1)+'.png')
    #         cards = identifyCards(im, DEBUG=True)
    #         self.assertEqual(len(cards), 2)

    # def test_detect_players(self):
    #     for i in range(3):
    #         im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
    #         p = PokerAnalyzer()
    #         p.table.cardSet = getTableCards(im, p.table.cardSet, DEBUG=False)
    #         p.table.cardSet = getTableCards(im, p.table.cardSet, DEBUG=False)
    #         p.table.cardSet.white_tone = getWhite(im, p.table.cardSet)
    #         p.detectTable(im, DEBUG=False)
    #         p.detectPlayers(im, DEBUG=False)
    #         p.show(im)

    # def test_detect_players(self):
    #     for i in range(4,5):
    #         x1,y1,x2,y2 = utils.select_window()
    #         #im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
    #         im = utils.cropped_screenshot(x1,y1,x2,y2)
    #         p = PokerAnalyzer()
    #         while p.initialScan(im):
    #         	pass
    #         print(p)
    #         #p.show(im)
    #
    #         p.refresh(im)
    #         print(p)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
