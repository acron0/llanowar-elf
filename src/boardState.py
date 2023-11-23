from .log import getLogger
from .ps import handleMessage
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
        self.player_id = None
        self.player_seat = None
        self.opponent_id = None
        self.opponent_seat = None
        #
        handleMessage('player_deck_list', self.handlePlayerDeckList)
        handleMessage('participants_identified', self.handleParticipantsIdentified)
        handleMessage('game_state_full', self.handleGameStateFull)
        handleMessage('game_state_diff', self.handleGameStateDiff)


    def __str__(self):
        output = "Current Board State:\n--------\nPlayer Cards:\n"
        output += sortedCardTable(self.player_cards)
        return output

    def handlePlayerDeckList(self, deck_list):
        for card in deck_list:
            self.player_cards.append(self.cardDb.getCard(card))
        self.logger.info("Received player's deck list")

    def handleParticipantsIdentified(self, player, opponent):
        self.player_id = player['id']
        self.player_seat = player['seat']
        self.opponent_id = opponent['id']
        self.opponent_seat = opponent['seat']
        self.logger.info("Received player and opponent seats: {0} ({1}) vs. {2} ({3})".format(self.player_id, self.player_seat, self.opponent_id, self.opponent_seat))

    def handleGameStateFull(self, game_state):
        self.logger.info("Received full game state")
        # update players first
        for player in game_state["players"]:
            pass

    def handleGameStateDiff(self, game_state):
        self.logger.info("Received game state diff")
        for key in game_state.keys():
            self.logger.debug(" - GameStateDiff key: {0}".format(key))
        self.logger.info(".")
