import unittest
import sys, cv2
from importlib import reload

sys.path.insert(0, r'C:\Users\manue\Documents\TFG\Holden\src')

import recognizeCard, detectTableCards
reload(recognizeCard)
reload(detectTableCards)
from recognizeCard import identifyCards
from detectTableCards import getTableCards

class RecognizeCardsTests(unittest.TestCase):

    def test_recognize_individual_cards(self):
        ncards = [5, 4, 5, 5, 2]
        for i in range(5):
            im = cv2.imread('../img/tables/table'+str(i+1)+'.png')
            card_set = getTableCards(im, None, DEBUG=False)
            card_set = getTableCards(im, card_set, DEBUG=False)
            self.assertEqual(len(card_set.cards), ncards[i])

    # TODO - Comprobar contenido y orden
    def test_recognize_player_cards(self):
        for i in range(4):
            im = cv2.imread('../img/playerCards/cardSet'+str(i+1)+'.png')
            cards = identifyCards(im, DEBUG=True)
            self.assertEqual(len(cards), 2)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
