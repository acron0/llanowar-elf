import requests
from log import getLogger
DEBOUNCE_MS = 75

# https://scryfall.com/docs/api


class ScryfallAPI():

    def __init__(self):
        self.logger = getLogger(__class__.__name__)
        #
        self.url = "https://api.scryfall.com/"
        self.headers = {}   
        
    def fetchFromApi(self, arenaId):
        try:
            req = requests.get(self.url + "cards/arena/" + str(arenaId))
        except Exception as e:
            self.logger.error("Error fetching card from Scryfall API: {0}".format(e))
        card_json = req.json()
        return card_json
        
