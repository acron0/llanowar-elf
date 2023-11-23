import json
from .log import getLogger
from .ps import handleMessage, sendMessage
import tailer


def isJson(line):
    try:
        json.loads(line)
        return True
    except:
        return False


class FileWatcher():

    def __init__(self, file_path, watch_mode='follow'):
        self.logger = getLogger(__class__.__name__)
        #
        self.watch_mode = watch_mode
        self.file_path = file_path
        self.json_buffer = []

    def processJsonBuffer(self, line):
        # is json? return it
        if isJson(line):
            return line
        # no buffer and line looks like json? start buffer
        elif len(self.json_buffer) == 0 and line.startswith("{"):
            # start buffer
            self.json_buffer = [line]
        # already started buffer? append to buffer
        elif len(self.json_buffer) > 0:
            self.json_buffer.append(line)
            # current line ends with }? check we have json
            if line.endswith("}"):
                possible_json = ''.join(self.json_buffer)
                if isJson(possible_json):
                    self.json_buffer = []
                    return possible_json
                else:
                    return None
            else:
                 # assume we're still building json
                return None
        # we aren't building json right now
        return line
    
    def processLine(self, line):
        clean_line = line.strip()
        if len(clean_line) > 0:
            processed_line = self.processJsonBuffer(clean_line)
            if processed_line is not None:
                sendMessage('new_log_line', line=processed_line)
    
    def start(self):
        if self.watch_mode == 'head':
            self.logger.info("Head mode only. Reading: {0} and then quitting".format(self.file_path))
            with open(self.file_path, 'r') as f:
                list(map(lambda line: self.processLine(line), f.readlines()))

        else:
            self.logger.info("Following log file: {0}".format(self.file_path))
            for line in tailer.follow(open(self.file_path)):
                self.processLine(line)
        
