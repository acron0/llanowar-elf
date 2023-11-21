import os
import configparser
from log import getLogger
import platform
class LogPathFinder:
    def __init__(self, ):
        self.logger = getLogger(__class__.__name__)

    def getLogPath(self):   
        self.logger.info("Searching for MTGA Player Log...")
        if platform.system().lower() == 'windows':
            app_data_dir = os.getenv("APPDATA")
            log = os.sep.join([app_data_dir[:-8], 'LocalLow', 'Wizards Of The Coast', 'MTGA', 'Player.log'])
            if(os.path.exists(log) == False):
                self.logger.fatal("Could not find MTGA Player log. Have you run the client yet?")
                return None
            else: 
                self.logger.info("Found MTGA Player log: {0}".format(log))
                return log
        elif platform.system().lower() == 'darwin':
            self.logger.fatal("Mac OS is not supported yet.")
            return None
        elif platform.system().lower() == 'linux':
            self.logger.fatal("Linux is not supported yet.")
            return None
        return None