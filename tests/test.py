import unittest
import sys, cv2, argparse
from importlib import reload

sys.path.insert(0, r'C:\Users\manue\Documents\TFG\Holden\src')

import recognizeCard, detectTableCards, pokerAnalyzer
reload(recognizeCard)
reload(detectTableCards)
reload(pokerAnalyzer)
from recognizeCard import identifyCards
from detectTableCards import getTableCards
from pokerAnalyzer import *

DEBUG = False

class TestCards(unittest.TestCase):
    def test_table_cards(self):
        print("")
        ncards = [4, 4, 5, 5, 5, 4]
        for i in range(6):
            im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
            card_set = getTableCards(im, None)
            card_set = getTableCards(im, card_set, DEBUG)
            self.assertEqual(len(card_set.cards), ncards[i])

    def test_overlapped_cards(self):
        print("")
        for i in range(4):
            im = cv2.imread('../img/playerCards/cardSet'+str(i+1)+'.png')
            cards = identifyCards(im, DEBUG)
            self.assertEqual(len(cards), 2)

    def test_player_cards(self):
        print("")
        im = cv2.imread('../img/tables/table5.png')
        p = PokerAnalyzer()
        p.context.player_cards_flag = True
        while p.initialScan(im):
            pass
        if DEBUG: p.show(im)

        im = cv2.imread('../img/tables/table7.png')
        p = PokerAnalyzer()
        p.context.player_cards_flag = True
        while p.initialScan(im):
            pass
        if DEBUG: p.show(im)

class TestPlayers(unittest.TestCase):
    def test_detect_players(self):
        print("")
        for i in range(3):
            im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
            p = PokerAnalyzer()
            p.table.cardSet = getTableCards(im, p.table.cardSet)
            p.table.cardSet.white_tone = getWhite(im, p.table.cardSet)
            p.detectTable(im)
            p.detectPlayers(im, DEBUG)

class TestAll(unittest.TestCase):
    def test_initial_scan(self):
        print("")
        for i in range(8):
            select = False
            if select:
                x1,y1,x2,y2 = utils.select_window()
                im = utils.cropped_screenshot(x1,y1,x2,y2)
            else:
                im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
            p = PokerAnalyzer()
            while p.initialScan(im):
            	pass
            if DEBUG: p.show(im)

def main(test, d):
    if d:
        global DEBUG
        DEBUG = d

    if test == "cards":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCards)
    elif test == "players":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayers)
    elif test == "all":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestAll)

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Test selector")
    parser.add_argument('test', type=str)
    parser.add_argument('-d','--debug', type=bool)
    args = parser.parse_args()

    main(args.test, args.debug)
