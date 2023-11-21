from watchdog.observers import Observer
from log import getLogger
from ps import sendMessage
import os
import time
import threading
import glob

def isLogFile(file_path):
    extension = os.path.splitext(file_path)[1]
    return extension == '.log'

def findLatestLogFile(path):
    # iterate through all files in the directory, starting with the newest
    files = list(filter(os.path.isfile, glob.glob(path + "/*")))
    files.sort(key=lambda x: -os.path.getmtime(x))
    for file_path in files:
        if isLogFile(file_path):
            return file_path

class DirWatcher(threading.Thread):
    def __init__(self, path):
        super().__init__()
        self.daemon = True
        self.path = path
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=True)
        self.observer.start()
        self.logger = getLogger(__class__.__name__)
        self.file_path = None

    def checkForNewFile(self):
        self.logger.debug("Checking for new log file in {0}".format(self.path))
        file_path = findLatestLogFile(self.path)
        if file_path is not None and file_path != self.file_path:
            self.file_path = file_path
            self.logger.info("Found a new log file: {0}".format(file_path))
            sendMessage('new_log_file', file_path=file_path)

    def run(self):
        self.logger.info("Watching {0}".format(self.path))
        self.checkForNewFile()
        while True:
            time.sleep(1)

    def dispatch(self, event):
        if event.event_type == 'created':
            self.logger.info("File created: {0}".format(event.src_path))
            self.checkForNewFile()
            
        else:
            #self.logger.debug("Ignoring event: {0}".format(event))
            return None