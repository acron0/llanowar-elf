from pubsub import pub
from .log import getLogger

logger = getLogger('pubsub')
trace = False

def sendMessage(topicName, **kwargs):
    if trace:
        logger.debug("Sending message -> {0} : {1}".format(topicName, kwargs))
    pub.sendMessage(topicName, **kwargs)

def handleMessage(topicName, handler):
    if trace:
        logger.debug("Added handler for {0}".format(topicName))
    pub.subscribe(handler, topicName)