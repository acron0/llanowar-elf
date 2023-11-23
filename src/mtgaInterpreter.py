
from .ps import handleMessage, sendMessage
from .log import getLogger
import json
import re

opening_line_regex = re.compile(r'^\[UnityCrossThreadLogger\].*')
client_event_regex = re.compile(r'.*Match to ([0-9A-Z]+)\: GreToClientEvent$')
match_game_room_state_changed_event_regex = re.compile(r'.*Match to ([0-9A-Z]+)\: MatchGameRoomStateChangedEvent$')

def handleGameStateEvent(logger, event):
    if event["gameStateMessage"]["type"] == "GameStateType_Diff":
        sendMessage('game_state_diff', game_state=event["gameStateMessage"])
    elif event["gameStateMessage"]["type"] == "GameStateType_Full":
        sendMessage('game_state_full', game_state=event["gameStateMessage"])
    else:
        logger.warning("Unhandled game state type: {0}".format(event["gameStateMessage"]["type"]))

def handleConnectionResponse(logger, event):
    sendMessage('player_deck_list', deck_list=event["connectResp"]["deckMessage"]["deckCards"])

class MTGAInterpreter:
    def __init__(self):
        self.logger = getLogger(__class__.__name__)
        #
        self.opening_line = None
        handleMessage('new_log_line', self.handleLine)

    def maybeHandleGameStateEvent(self, opening_line, data):
        match = client_event_regex.match(opening_line)
        if match is not None:
            for msg in data["greToClientEvent"]["greToClientMessages"]:
                if msg['type'] == 'GREMessageType_GameStateMessage':
                    handleGameStateEvent(self.logger, msg)
                elif msg['type'] == 'GREMessageType_ConnectResp':
                    handleConnectionResponse(self.logger, msg)
                else:
                    pass
                    self.logger.debug("Unhandled message type: {0}".format(msg['type']))

    def maybeHandleRoomStateEvent(self, opening_line, data):
        match = match_game_room_state_changed_event_regex.match(opening_line)
        if match is not None:
            player_id = match.group(1)
            opponent_id = None
            player_seat = None
            opponent_seat = None

            players = data["matchGameRoomStateChangedEvent"]["gameRoomInfo"]["players"]
            for player in players:
                if player["userId"] != player_id:
                    opponent_id = player["userId"]
                    opponent_seat = player["systemSeatId"]
                else:
                    player_seat = player["systemSeatId"]
            sendMessage('participants_identified', player={'id': player_id, 'seat': player_seat}, opponent={'id': opponent_id, 'seat': opponent_seat})

        
    def handleNewLogData(self, opening_line, data=None):
        if data is not None:
            self.maybeHandleGameStateEvent(opening_line, data)
            self.maybeHandleRoomStateEvent(opening_line, data)
            
        
    def handleLine(self, line):
        if self.opening_line is None:
            # does this line match our regex for opening lines?
            match = opening_line_regex.match(line)
            if match:
                self.opening_line = line
        else:
            # is the next line valid json?
            try:
                json_data = json.loads(line)
                self.handleNewLogData(opening_line=self.opening_line, data=json_data)
                self.opening_line = None
            except:
                self.handleNewLogData(opening_line=self.opening_line)
                self.opening_line = None
                self.handleLine(line) # because now we have a new opening line
    
    