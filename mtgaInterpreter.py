
from ps import handleMessage, sendMessage
from log import getLogger
import json
import re

opening_line_regex = re.compile(r'^\[UnityCrossThreadLogger\].*')
client_event_regex = re.compile(r'.*Match to ([0-9A-Z])+\: GreToClientEvent$')

def handleGameStateEvent(logger, event):
    #logger.debug("Event: {0}".format(event))
    pass

def handleConnectionResponse(logger, event):
    sendMessage('player_deck_list', deck_list=event["connectResp"]["deckMessage"]["deckCards"])

class MTGAInterpreter:
    def __init__(self):
        self.logger = getLogger(__class__.__name__)
        #
        self.player_id = None
        self.opening_line = None
        handleMessage('new_log_line', self.handleLine)
        
    def handleNewLogData(self, opening_line, data=None):
        if data is not None:
            match = client_event_regex.match(opening_line)
            if match is not None:
                self.player_id = match.group(1)
                for msg in data["greToClientEvent"]["greToClientMessages"]:
                    if msg['type'] == 'GREMessageType_GameStateMessage':
                        handleGameStateEvent(self.logger, msg)
                    if msg['type'] == 'GREMessageType_ConnectResp':
                        handleConnectionResponse(self.logger, msg)
                    else:
                        pass
                        self.logger.debug("Unhandled message type: {0}".format(msg['type']))
        
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
    
    