from log import getLogger
from ps import handleMessage
from itertools import groupby
from collections import Counter
from prettytable import PrettyTable

def sortedCardTable(cards):
    table = PrettyTable()
    table.field_names = ["Name", "Count", "Cost", "Type"]
    table.align["Name"] = "l"

    # pick fields from card
    card_frequencies = Counter(cards)

    def cardToRow(card, count):
        return [card["name"], count, card.manaCost(), card["type_line"], card["cmc"]]
    
    rows = [cardToRow(card, count) for card, count in card_frequencies.items()]
    rows.sort(key=lambda row: row[-1]) # sort by cmc
    trimmed_rows = [row[:-1] for row in rows] # remove cmc

    table.add_rows(trimmed_rows)
    return table.get_string()

class MTGABoardState():

    def __init__(self, cardDb):
        self.logger = getLogger(__class__.__name__)
        self.cardDb = cardDb
        #
        self.player_cards = []
        #
        handleMessage('player_deck_list', self.handlePlayerDeckList)

    def __str__(self):
        output = "Current Board State:\n--------\nPlayer Cards:\n"
        output += sortedCardTable(self.player_cards)
        return output

    def handlePlayerDeckList(self, deck_list):
        self.player_cards = []
        for card in deck_list:
            self.player_cards.append(self.cardDb.getCard(card))
        self.logger.info("Received deck list")
