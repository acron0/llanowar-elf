import json
import threading
from log import getLogger
from mtgCard import MTGCard

CARD_CACHE_FILE_NAME = '.card_cache.json'

class MTGACardDB():

    def __init__(self, api):
        self.logger = getLogger(__class__.__name__)
        #
        self.api = api
        self.card_cache = self.readCache()
        #
        self.scheduled = None

    def scheduleCardCacheWrite(self):
        if self.scheduled:
            self.scheduled.cancel()
        self.scheduled = threading.Timer(5.0, self.writeCache()).start()

    def writeCache(self):
        self.logger.info('Writing card cache to disk: {0}'.format(CARD_CACHE_FILE_NAME))
        with open(CARD_CACHE_FILE_NAME, 'w') as file:
            file.write(json.dumps(self.card_cache))

    def readCache(self):
        try:
            with open(CARD_CACHE_FILE_NAME, 'r') as file:
                return json.loads(file.read())
        except FileNotFoundError:
            self.logger.info('No card cache found, starting from scratch')
            return {}

    def getCard(self, cardId):
        cardIdStr = str(cardId)
        if cardIdStr in self.card_cache:
            return MTGCard(self.card_cache[cardIdStr])
        else:
            card = self.api.fetchFromApi(cardId)
            self.card_cache[cardIdStr] = card
            self.scheduleCardCacheWrite()
            return card
