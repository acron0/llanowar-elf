class MTGCard():
    def __init__(self, obj) -> None:
        self.card = obj

    def __getitem__(self, key):
        return self.card[key]
    
    def __hash__(self):
        return hash(self.card["id"])
    
    def __eq__(self, other):
        if isinstance(other, MTGCard):
            return self.card["id"] == other.card["id"]
        return False
    
    def manaCost(self):
        if 'mana_cost' in self.card:
            return self.card['mana_cost']
        else:
            # check faces
            return self.card["card_faces"][0]["mana_cost"]