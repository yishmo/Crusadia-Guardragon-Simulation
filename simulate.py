import random
import deck

bool1 = 0
bool2 = 0
bool3 = 0
bool4 = 0
bool5 = 0
bool6 = 0
def can_combo(hand):
    firstCrusadia = None
    for i in range(len(hand)):
        if 'Crusadia' in hand[i].name or 'rota' == hand[i].name:
            firstCrusadia = hand[i]
            del hand[i]
            break
    if firstCrusadia is not None:
        for card in hand:
            if isExtender(card, firstCrusadia):
                return True
     

    return False

def isExtender(card, firstCrusadia):
    global bool1
    global bool2
    global bool3
    global bool4
    global bool5
    global bool6
    if 'Crusadia' in card.name:
        if firstCrusadia.name == 'Crusadia Draco' and card.name == 'Crusadia Draco':
            bool1 += 1
        else:
            bool2 += 1
            return True
        

    elif 'Ranryu' == card.name or 'rota' == card.name or 'world legacy succession' == card.name or 'monster reborn' == card.name:
        bool3 += 1
        return True
    elif 'quik launch' == card.name:
        if inDeck('rokket tracer', deck[5:]):
            bool4 += 1
            return True
    elif 'black dragon' == card.name:
        if firstCrusadia.name == 'Crusadia Maximus':
            bool5 += 1
            return True

    elif 'world legacy guardragon' == card.name:
        if firstCrusadia.name == 'Crusadia Draco':
            bool6 += 1
            return True

    return False


def inDeck(name, deck):
    for c in deck:
        if name == c.name:
            return True

    return False
        
            
    
with open('CG.ygo') as file:
    deck = deck.deck_from_file(file)

success = 0
fail = 0
for i in range(1000000):
    random.shuffle(deck)
    hand = deck[0:5]
    if can_combo(hand):
        success += 1
    else:
        fail += 1
        #for card in hand:
        #    print(card.name, fail)

print(success/(success + fail))
print(bool1, bool2, bool3, bool4, bool5, bool6)
