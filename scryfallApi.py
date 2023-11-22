import time
import requests
from log import getLogger

DEBOUNCE_MS = 75

class ScryfallAPI():
    def __init__(self):
        self.logger = getLogger(__class__.__name__)
        #
        self.url = "https://api.scryfall.com/"
        self.headers = {}
        self.last_call_time = 0

    def fetchFromApi(self, arenaId):
        current_time = time.time() * 1000  # Convert to milliseconds
        time_since_last_call = current_time - self.last_call_time

        if time_since_last_call < DEBOUNCE_MS:
            time_to_wait = DEBOUNCE_MS - time_since_last_call
            time.sleep(time_to_wait / 1000)  # Convert to seconds

        try:
            req = requests.get(self.url + "cards/arena/" + str(arenaId))
        except Exception as e:
            self.logger.error("Error fetching card from Scryfall API: {0}".format(e))

        card_json = req.json()
        self.last_call_time = time.time() * 1000  # Update last call time
        return card_json
        
