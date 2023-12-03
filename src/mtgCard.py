class MTGCard():
    def __init__(self, obj) -> None:
        self.card = obj
    
    def __hash__(self):
        return hash(self.card["id"])
    
    def __eq__(self, other):
        if isinstance(other, MTGCard):
            return self.card["id"] == other.card["id"]
        return False
    
    def id(self):
        if 'id' in self.card:
            return self.card['arena_id']
        else:
            return 0
    
    def typeLine(self):
        if 'type_line' in self.card:
            return self.card['type_line']
        else:
            return 'unknown'
        
    def name(self):
        if 'name' in self.card:
            return self.card['name']
        else:
            return 'Unknown'
        
    def cmc(self):
        if 'cmc' in self.card:
            return self.card['cmc']
        else:
            return 'n/a'
    
    def manaCost(self):
        if 'mana_cost' in self.card:
            return self.card['mana_cost']
        elif 'card_faces' in self.card:
            # check faces
            return self.card["card_faces"][0]["mana_cost"]
        else:
            return 'n/a'