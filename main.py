import platform

from fileWatcher import FileWatcher
from log import getLogger
from logPathFinder import LogPathFinder
from mtgaBoardState import MTGABoardState
from mtgaCardDb import MTGACardDB
from mtgaInterpreter import MTGAInterpreter
from scryfallApi import ScryfallAPI

log_path_override = 'example.log'
watch_mode = 'head'


def run():
    version = '?.?.?'
    with open('VERSION', 'r') as file:
        version = file.read()
    #
    logger = getLogger(__name__)
    logger.info('MTGAI {0} - {1}'.format(version, platform.system()))

    # we need the log dir to even begin.
    if log_path_override:
        log_path = log_path_override
    else:
        lpf = LogPathFinder()
        log_path = lpf.getLogPath()

    if log_path is None:
        exit(1)

    #
    watcher = FileWatcher(log_path, watch_mode=watch_mode)
    interpreter = MTGAInterpreter()
    api = ScryfallAPI()
    cardDb = MTGACardDB(api)
    board = MTGABoardState(cardDb)

    try:
        watcher.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info('Received keyboard interrupt, quitting.')

    print(board)

if __name__ == '__main__':
    run()
    
