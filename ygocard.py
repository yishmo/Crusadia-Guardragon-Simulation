class Card:
    def __init__(self, name):
        self.name = name

class MonsterCard(Card):
    def __init__(self, name, level, type, attribute):
        super().__init__(name)
        self.level = level
        self.type = type
        self.attribute = attribute
        
class SpellCard(Card):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

class TrapCard(Card):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

class Blank:
    def __init__(self):
        pass
    def __getattr__(self, name):
        return "Blank"
