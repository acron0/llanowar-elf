from .log import getLogger
from .zone import Zone

class MTGPlayer():
    def __init__(self, ):
        self.logger = getLogger(__class__.__name__)
        # identification
        self.id = None
        self.seat = None
        self.name = None
        #
        self.life_total = 0
        self.max_hand_size = 7
        #
        self.zones = {}

    def identity(self):
        return "{0} ({1} // {2})".format(self.name, self.seat, self.id)

    def update(self, player):
        self.life_total = player["lifeTotal"]
        self.max_hand_size = player["maxHandSize"]

    def updateZone(self, zone_id, zone_type, object_instance_ids):
        self.zones[zone_id] = Zone(zone_type, object_instance_ids)

    # some zone shortcuts
    def zoneByType(self, zone_type):
        for zone in self.zones.values():
            if zone.type == zone_type:
                return zone

    def library(self):
        return self.zoneByType('ZoneType_Library')
    
    def hand(self):
        return self.zoneByType('ZoneType_Hand')

        