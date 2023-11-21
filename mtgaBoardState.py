from log import getLogger
from ps import handleMessage


class MTGABoardState():

    def __init__(self, cardDb):
        self.logger = getLogger(__class__.__name__)
        self.cardDb = cardDb
        #
        self.player_cards = []
        #
        handleMessage('player_deck_list', self.handlePlayerDeckList)

    def handlePlayerDeckList(self, deck_list):
        self.player_cards = []
        for card in deck_list:
            self.player_cards.append(self.cardDb.getCard(card))
        self.logger.info("Received deck list")
