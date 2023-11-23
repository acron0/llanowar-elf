import logging
import logging.config

logging.config.fileConfig('conf/log.conf')

def getLogger(name):
    """Returns a configured logger"""
    return logging.getLogger(name)
