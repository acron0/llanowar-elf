from log import getLogger


class MTGACardDB():

    def __init__(self, api):
        self.logger = getLogger(__class__.__name__)
        #
        self.api = api
        self.card_cache = {}
        
    def getCard(self, cardId):
        if cardId in self.card_cache:
            return self.card_cache[cardId]
        else:
            card = self.api.fetchFromApi(cardId)
            self.card_cache[cardId] = card
            return card
