from .log import getLogger
from .ps import handleMessage
from .mtgPlayer import MTGPlayer
from .mtgCard import MTGCard
from .zone import Zone
from itertools import groupby
from collections import Counter
from prettytable import PrettyTable

def sortedCardTable(cards):
    table = PrettyTable()
    table.field_names = ["Name", "Count ({0})".format(len(cards)), "Cost", "Type"]
    table.align["Name"] = "l"

    # pick fields from card
    card_frequencies = Counter(cards)

    def cardToRow(card, count):
        if card:
            return [card.name(), count, card.manaCost(), card.typeLine(), card.cmc()]
        else:
            return []
    
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
        self.player = MTGPlayer()
        self.opponent = MTGPlayer()
        #self.active_seat = None
        #self.decision_seat = None
        #
        self.known_cards = []
        self.gameObjects = {}
        self.battlefield = None
        #
        handleMessage('player_deck_list', self.handlePlayerDeckList)
        handleMessage('participants_identified', self.handleParticipantsIdentified)
        handleMessage('game_state_full', self.handleGameStateFull)
        handleMessage('game_state_diff', self.handleGameStateDiff)

    def playerBySeat(self, seat):
        if seat == self.player.seat:
            return self.player
        elif seat == self.opponent.seat:
            return self.opponent
        else:
            self.logger.error("Unknown seat: {0}".format(seat))
            return None
    
    def cardById(self, id):
        for card in self.known_cards:
            if card.id() == id:
                return card
        card = self.cardDb.getCard(id)
        self.known_cards.append(card)
        return card
    
    def extractCardsFromZone(self, zone):
        cards = []
        if zone:
            for objId in zone.object_instance_ids:
                if objId in self.gameObjects:
                    card = self.cardById(self.gameObjects[objId]["grpId"])
                    cards.append(card)
                else:
                    cards.append(MTGCard({"name": "Unknown", "type_line": "Unknown", "id":"unknown", "cmc": "n/a"}))
        return cards

    def handlePlayerDeckList(self, deck_list):
        for card in deck_list:
            self.known_cards.append(self.cardDb.getCard(card))
        self.logger.info("Updated known cards (total: {0})".format(len(self.known_cards)))

    def handleParticipantsIdentified(self, player, opponent):
        self.player.id = player['userId']
        self.player.name = player['playerName']
        self.player.seat = player['systemSeatId']

        self.opponent.id = opponent['userId']
        self.opponent.seat = opponent['systemSeatId']
        self.opponent.name = opponent['playerName']

        self.logger.info("Received player and opponent seats: {0} vs. {1}".format(self.player.identity(), self.opponent.identity()))

    def updatePlayers(self, game_state):
        if "players" in game_state:
            for player in game_state["players"]:
                self.playerBySeat(player["controllerSeatId"]).update(player)

    def updateZones(self, game_state):
        if "zones" in game_state:
            for zone in game_state["zones"]:
                if "objectInstanceIds" in zone:
                    if 'ownerSeatId' in zone:
                        self.playerBySeat(zone["ownerSeatId"]).updateZone(zone["zoneId"], zone["type"], zone["objectInstanceIds"])
                    elif zone["type"] == 'ZoneType_Battlefield':
                        self.battlefield = Zone(zone["type"], zone["objectInstanceIds"])
                    else:
                        self.logger.warning("Zone with no owner: {0}".format(zone))

    def updateGameObjects(self, game_state):
        if "gameObjects" in game_state:
            for obj in game_state["gameObjects"]:
                self.logger.debug("Updating game object: {0} - {1}".format(obj["grpId"], obj["type"]))
                self.gameObjects[obj["instanceId"]] = obj


    def handleGameStateFull(self, game_state):
        self.logger.info("Received full game state")
        # update players
        self.updatePlayers(game_state)
        # update zones
        self.updateZones(game_state)    

    def handleGameStateDiff(self, game_state):
        self.logger.info("Received game state diff")
        # update game objects
        self.updateGameObjects(game_state)
        # update players
        self.updatePlayers(game_state)
        # update zones
        self.updateZones(game_state)
        # # update active seat
        # if "turnInfo" in game_state:
        #     self.active_seat = game_state["turnInfo"]["activePlayer"]
        #     self.decision_seat = game_state["turnInfo"]["decisionPlayer"]
    
        # print board state
        self.logger.info(str(self))
        pass

    def __str__(self):
        output = "Current Board State:\n--------\nPlayer's Library:\n"
        playerLibrary = self.extractCardsFromZone(self.player.library())
        output += sortedCardTable(playerLibrary)
        output += "\n--------\nPlayer's Hand:\n"
        playerHand = self.extractCardsFromZone(self.player.hand())
        output += sortedCardTable(playerHand)
        output += "\n--------\nBattlefield:\n"
        battlefield = self.extractCardsFromZone(self.battlefield)
        output += sortedCardTable(battlefield)
        return output
