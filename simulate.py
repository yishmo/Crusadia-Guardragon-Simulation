import random
import itertools
import ygodeck
import ygocard
import cardnames as cn
import sys
import math
import time
import os
from collections import defaultdict

NUM_HANDS = 100 
NUM_SAMPLE_MEANS = 101
DECK_FILE_NAME = 'CG.ygo'



COMBO_POINTS = 9
WATERFRONT_POINTS = 4.5
AZATHOT_POINTS = 3

CASE2 = COMBO_POINTS
CASE3 = COMBO_POINTS + AZATHOT_POINTS
CASE4 = COMBO_POINTS + WATERFRONT_POINTS
CASE5 = COMBO_POINTS + AZATHOT_POINTS + WATERFRONT_POINTS
#no need for case 1 since it is always worth 0

usedTerraforming = False #a boolean to keep track if you used terraforming

debug = False
dontShuffle = False

hand = []
deck = []
graveyard = []


#this variable is the list you use to rank decks:
ALL_DECK_NAMES = [('./ten/ten2.ygo', 5582),
                ('./nine/nine5.ygo', 5544),
                ('./eight/eight5.ygo', 5526),
                ('./eleven/eleven2.ygo', 5463),
                ('./nine/nine2.ygo', 5456),
                ('./nine/nine1.ygo', 5372),
                ('./seven/seven2.ygo', 5288),
                ('./eight/eight1.ygo', 5224), 
                ('./five/five5.ygo', 5133),
                ('./eleven/eleven3.ygo', 5109), 
                ('./ten/ten4.ygo', 5075),
                ('./nine/nine3.ygo', 5067),
                ('./six/six2.ygo', 5045),
                ('./eight/eight2.ygo', 4991),
                ('./ten/ten5.ygo', 4989),
                ('./ten/ten7.ygo', 4978),
                ('./five/five3.ygo', 4972),
                ('./eight/eight3.ygo', 4938),
                ('./eleven/eleven5.ygo', 4922),
                ('./six/six3.ygo', 4861),
                ('./four/four2.ygo', 4811),
                ('./five/five2.ygo', 4805),
                ('./nine/nine8.ygo', 4755),
                ('./three/three5.ygo', 4752),
                ('./seven/seven3.ygo', 4724),
                ('./ten/ten1.ygo', 4710),
                ('./twelve/twelve1.ygo', 4675),
                ('./eight/eight7.ygo', 4668),
                ('./seven/seven5.ygo', 4664),
                ('./eleven/eleven1.ygo', 4641),
                ('./seven/seven7.ygo', 4624),
                ('./seven/seven8.ygo', 4612),
                ('./nine/nine4.ygo', 4606),
                ('./seven/seven1.ygo', 4594),
                ('./ten/ten3.ygo', 4525),
                ('./three/three2.ygo', 4515),
                ('./twelve/twelve3.ygo', 4506),
                ('./four/four1.ygo', 4502),
                ('./four/four5.ygo', 4497),
                ('./two/two5.ygo', 4494),
                ('./five/five8.ygo', 4433),
                ('./nine/nine7.ygo', 4418),
                ('./six/six5.ygo', 4417),
                ('./five/five1.ygo', 4413),
                ('./eight/eight8.ygo', 4376),
                ('./ten/ten6.ygo', 4367),
                ('./nine/nine6.ygo', 4281),
                ('./three/three3.ygo', 4278),
                ('./three/three7.ygo', 4253),
                ('./five/five7.ygo', 4252),
                ('./one/one2.ygo', 4243),
                ('./eight/eight4.ygo', 4230),
                ('./six/six7.ygo', 4195),
                ('./two/two2.ygo', 4135),
                ('./eight/eight6.ygo', 4106),
                ('./six/six6.ygo', 4069),
                ('./four/four3.ygo', 4059),
                ('./eleven/eleven4.ygo', 4047),
                ('./four/four8.ygo', 4037),
                ('./six/six1.ygo', 4033),
                ('./three/three8.ygo', 4020),
                ('./seven/seven4.ygo', 4009),
                ('./twelve/twelve2.ygo', 3999),
                ('./four/four7.ygo', 3941),
                ('./five/five6.ygo', 3897),
                ('./six/six8.ygo', 3863),
                ('./four/four4.ygo', 3811),
                ('./five/five4.ygo', 3760),
                ('./three/three1.ygo', 3690),
                ('./seven/seven6.ygo', 3635),
                ('./four/four6.ygo', 3509),
                ('./two/two1.ygo', 3498),
                ('./six/six4.ygo', 3458),
                ('./two/two7.ygo', 3405),
                ('./one/one1.ygo', 3383),
                ('./two/two3.ygo', 3382),
                ('./three/three4.ygo', 3372),
                ('./one/one7.ygo', 3362),
                ('./one/one5.ygo', 3254),
                ('./two/two8.ygo', 3253),
                ('./three/three6.ygo', 3233),
                ('./one/one8.ygo', 3138),
                ('./one/one6.ygo', 2980),
                ('./two/two6.ygo', 2971),
                ('./one/one3.ygo', 2950),
                ('./two/two4.ygo', 2936), 
                ('./one/one4.ygo', 2534)]
                



def can_combo():
    global usedTerraforming
    usedTerraforming = False
    firstCrusadia = None
    foundIndex = None
    for i in range(len(hand)):
        if 'CRUSADIA' in hand[i].name or cn.ROTA_STR == hand[i].name:
            firstCrusadia = hand[i]
            foundIndex = i #keep track of this so we don't count this as an extender
            break

    if firstCrusadia is not None:
        for i in range(len(hand)):
            if isExtender(hand[i], firstCrusadia) and i != foundIndex:
                return True
     

    return check_for_ravine_plays()

def isExtender(card, firstCrusadia):
    if 'CRUSADIA' in card.name:
        if firstCrusadia.name == cn.CRU_DRA_STR and card.name == cn.CRU_DRA_STR:
            #black dragon and destrudo are actually exceptions to this rule
            #since you can use magius in the graveyard
            #otherwise the algorithm will just find the other normal extender
            if inHand(cn.DESTRUDO_STR) or inHand(cn.BLACK_DRA_STR):
                return True

        else:
            return True
        

    elif cn.RANRYU_STR == card.name or cn.ROTA_STR == card.name or cn.WLS_STR == card.name or cn.REBORN_STR == card.name or cn.INARI_STR == card.name or cn.JIGABYTE_STR == card.name or cn.NEFARIOUS_STR == card.name:
        return True
    elif cn.QUICK_STR == card.name:
        if inDeck(cn.ROKKET_STR):
            return True
    elif cn.BLACK_DRA_STR == card.name:
        if firstCrusadia.name == cn.CRU_MAX_STR or inHand(cn.THRASHER_STR):
            return True

    elif cn.DESTRUDO_STR == card.name and inHand(cn.THRASHER_STR):
        return True

    elif (cn.TERRA_STR == card.name or cn.RAVINE_STR == card.name) and inHand(cn.THRASHER_STR): #set rotation work later
        return True

    elif cn.WLG_STR == card.name:
        if firstCrusadia.name == cn.CRU_DRA_STR:
            return True

    return False

def isUnconditionalExtender(card):
    if (cn.RANRYU_STR == card.name or cn.WLG_STR == card.name or cn.WLS_STR == card.name 
        or cn.REBORN_STR == card.name or cn.INARI_STR == card.name or cn.JIGABYTE_STR == card.name or cn.NEFARIOUS_STR == card.name):
        return True
    elif cn.QUICK_STR == card.name:
        if inDeck(cn.ROKKET_STR):
            return True

    return False

def can_make_azathot_helper(testHand):
    global grave
    for i in range(len(testHand)):
        if 'CRUSADIA' in testHand[i].name:
            grave.append(testHand[i])
            del testHand[i]#we can delete because these are copies
            break
        
        elif cn.ROTA_STR == testHand[i].name:
            grave.append(ygocard.MonsterCard(cn.CRU_ARB_STR, '3', 'warrior', 'water'))
            del testHand[i]
            break

    return testHand

def can_make_azathot(fourCardHand):
    zoneOccupied = False
    firstMaterial = None
    graveUsed = False
    for card in fourCardHand:
        
        if cn.CRU_DRA_STR == card.name:
            if firstMaterial is None:
                cond1 = False
                cond2 = False
                for card in hand:
                    if isDracoExtender(card) and not cond1: #if we've found a draco extender we look for a generic one
                        cond1 = True
                    elif isAzathotExtender(card) and not cond2:
                        cond2 = True

                return cond1 and cond2

            else:
                return False 
        elif cn.RANRYU_STR == card.name or cn.JIGABYTE_STR == card.name or cn.THRASHER_STR == card.name or cn.INARI_STR == card.name or cn.NEFARIOUS_STR == card.name:
            if firstMaterial is None:
                firstMaterial = card
            elif firstMaterial.name == card.name:
                pass #cant have two of the same
            else:
                return True

        elif cn.ROTA_STR == card.name and inDeck(cn.THRASHER_STR):
            if firstMaterial is None:
                firstMaterial = card
            else:
                return True

        elif cn.REBORN_STR == card.name and levelInGrave('4') and not graveUsed:
            if firstMaterial is None:
                firstMaterial = card
                graveUsed = True
            else:
                return True
                
        elif cn.WLS_STR == card.name and levelInGrave('4') and not zoneOccupied and not graveUsed:
            if firstMaterial is None:
                firstMaterial = card
                graveUsed = True
            else:
                return True

        elif cn.WLG_STR == card.name and inGrave(cn.CRU_DRA_STR) and not graveUsed:
            if firstMaterial is None:
                firstMaterial = card
                graveUsed = True
            else:
                return True
            
        elif cn.CRU_MAX_STR == card.name and not zoneOccupied:
            if firstMaterial is None:
                firstMaterial = card
            else:
                return True

        elif cn.DESTRUDO_STR == card.name and levelInGrave('3'):
            if firstMaterial is None:
                firstMaterial = card
            else:
                return True

        elif (cn.RAVINE_STR == card.name or (cn.TERRA_STR == card.name and inHand(cn.WATERFRONT_STR))) and levelInGrave('3') and inDeck(cn.DESTRUDO_STR):
            if firstMaterial is None:
                firstMaterial = card
            else:
                return True

        elif cn.BLACK_DRA_STR== card.name and attributeInGrave('light'):
            if firstMaterial is None:
                firstMaterial = card
            else:
                return True

        elif cn.QUICK_STR == card.name and inDeck(cn.ROKKET_STR):
            if firstMaterial is None:
                firstMaterial = card
                deckToGrave(cn.ROKKET_STR)
            else:
                return True



    return False

def check_for_ravine_plays():
    #you could be desparate, in which case a dragon ravine/terraforming + a revival spell works
    #**let's assume you dump draco every time so that it works with WLGuardragon, even though
    #this is a slight simplification
    if inHand(cn.RAVINE_STR) and (inHand(cn.REBORN_STR) or inHand(cn.WLG_STR) or inHand(cn.WLS_STR)):
        if inHand(cn.REBORN_STR):
            revivalIndex = indexInHand(cn.REBORN_STR)
        elif inHand(cn.WLG_STR):
            revivalIndex = indexInHand(cn.WLG_STR)
        else:
            revivalIndex = indexInHand(cn.WLS_STR)

        for i in range(len(hand)):
            if isUnconditionalExtender(hand[i]) and i != revivalIndex:
                return True
        
    elif inHand(cn.TERRA_STR) and inDeck(cn.RAVINE_STR) and (inHand(cn.REBORN_STR) or inHand(cn.WLG_STR) or inHand(cn.WLS_STR)):
        usedTerraforming = True
        if inHand(cn.REBORN_STR):
            revivalIndex = indexInHand(cn.REBORN_STR)
        elif inHand(cn.WLG_STR):
            revivalIndex = indexInHand(cn.WLG_STR)
        else:
            revivalIndex = indexInHand(cn.WLS_STR)

        for i in range(len(hand)):
            if isUnconditionalExtender(hand[i]) and i != revivalIndex:
                return True
    return False


#a special kind of extender. If you use draco for azathot you need to be able to 
#ss a dragon at the end to do saryuja combo:
def isDracoExtender(card):
    if (card.name == cn.WHITE_DRA_STR or card.name == cn.BLACK_DRA_STR or card.name == cn.RANRYU_STR or
        card.name == cn.REBORN_STR or card.name == cn.WLS_STR or 
        card.name == cn.WLG_STR or (card.name == cn.QUICK_STR and 
        inDeck(cn.ROKKET_STR)) or cn.DESTRUDO_STR == card.name and levelInGrave('3') or 
        (cn.RAVINE_STR == card.name or (cn.TERRA_STR == card.name and inHand(cn.WATERFRONT_STR))) #*this is only applicable if you value waterfront more than azathot
        and levelInGrave('3') and inDeck(cn.DESTRUDO_STR)):
        
        return True
    return False

def isAzathotExtender(card, zoneOccupied = False):
            
        if ((cn.RANRYU_STR == card.name or cn.JIGABYTE_STR == card.name or cn.THRASHER_STR == card.name or cn.INARI_STR == card.name or cn.NEFARIOUS_STR == card.name)
            or (cn.ROTA_STR == card.name and inDeck(cn.THRASHER_STR))
            or (cn.REBORN_STR == card.name and levelInGrave('4'))
            or (cn.WLS_STR == card.name and levelInGrave('4') and not zoneOccupied)
            or (cn.WLG_STR == card.name and inGrave(cn.CRU_DRA_STR))
            or (cn.CRU_MAX_STR == card.name and not zoneOccupied)
            or (cn.DESTRUDO_STR == card.name and levelInGrave('3'))
            or ((cn.RAVINE_STR == card.name or (cn.TERRA_STR == card.name and inHand(cn.WATERFRONT_STR))) and levelInGrave('3') and inDeck(cn.DESTRUDO_STR))
            or (cn.BLACK_DRA_STR== card.name and attributeInGrave('light'))
            or(cn.QUICK_STR == card.name and inDeck(cn.ROKKET_STR))):

            return True

        return False

def attributeInGrave(attribute):
    for card in grave:
        if card.attribute == attribute:
            return True

    return False

def levelInGrave(level):
    for card in grave:
        if card.level == level:
            return True

    return False

def deckToGrave(name):
    for i in range(len(deck)):
        if name == deck[i].name:
            grave.append(deck[i])
            del deck[i]
            return
    raise AttributeError(name, 'was not in deck')
     
def graveToDeck(name):
    for i in range(len(grave)):
        if name == grave[i].name:
            deck.append(grave[i])
            del grave[i]
            return
    raise AttributeError(name, 'was not in grave')

def deckToHand(name):
    for i in range(len(deck)):
        if name == deck[i].name:
            hand.append(deck[i])
            del deck[i]
            return
    raise AttributeError(name, 'was not in deck')

def handToGrave(name):
    for i in range(len(hand)):
        if name == hand[i].name:
            grave.append(hand[i])
            del hand[i]
            return
    raise AttributeError(name, 'was not in hand')

def inDeck(name):
    for c in deck:
        if name == c.name:
            return True

    return False

def inGrave(name):
    for c in grave:
        if name == c.name:
            return True

    return False

def inHand(name):
    for c in hand:
        if name == c.name:
            return True

    return False

def indexInHand(name):
    for i in range(len(hand)):
        if name == hand[i].name:
            return i

    raise AttributeError(name, 'was not in hand')

def contains_waterfront():
    firstNine = list(hand + deck[0:4])
    for c in firstNine:
        if c.name == cn.WATERFRONT_STR or c.name == cn.TERRA_STR or (c.name == cn.SET_ROTATION_STR and inDeck(cn.RAVINE_STR)):
            return True

    #well we tried an easy check, now lets remove
    #draco and REDMD(or destrudo if we already have it)
    #from our decks to check for

    if inDeck(cn.REDMD_STR):
        deckToGrave(cn.REDMD_STR)
        graveToDeck(cn.REDMD_STR)#puts on bottom of deck so we don't draw it
    else:
        if inDeck(cn.DESTRUDO_STR):
            deckToGrave(cn.DESTRUDO_STR)
            graveToDeck(cn.DESTRUDO_STR)#puts on bottom of deck so we don't draw it

    if inDeck(cn.CRU_DRA_STR):
        deckToGrave(cn.CRU_DRA_STR)
        graveToDeck(cn.CRU_DRA_STR)#puts on bottom of deck so we don't draw it


    for card in firstNine:
        if (card.type == 'dragon' and card.name != cn.REDMD_STR) or card.name == cn.QUICK_STR or isRevivalSpell(card):
            #well then we get to see an extra 4 cards
            for card in deck[4:8]:
                if card.name == cn.WATERFRONT_STR or card.name == cn.TERRA_STR or (card.name == cn.SET_ROTATION_STR and inDeck(cn.RAVINE_STR)):
                    return True 

    return False

def isRevivalSpell(card):
    return card.name == cn.REBORN_STR or card.name == cn.WLG_STR or card.name == cn.WLS_STR
        
        


def average_point_value(case):        
    total = 0
    for k,v in case.items():
        if k == 1:
            pass
        elif k == 2:
            total += v * CASE2
        elif k == 3:
            total += v * CASE3
        elif k == 4:
            total += v * CASE4
        elif k == 5:
            total += v * CASE5

    return total/NUM_HANDS

            
def reset(originalDeck):
    global hand
    global deck
    global grave
    
    if dontShuffle:
        pass
    else:
        random.shuffle(originalDeck)
    hand = originalDeck[0:5]
    deck = originalDeck[5:]
    grave = []

def run_simulation(deckFileName):
    global hand
    global deck
    global grave

    comboSuccess = 0
    waterfrontSuccess = 0
    azathotSuccess = 0

    case = defaultdict(int)

    with open(deckFileName) as file:
        originalDeck = ygodeck.deck_from_file(file)

    reset(originalDeck) #this function is used to restart the game

    print('Deck has', len(originalDeck), 'cards.')
    print(NUM_HANDS, 'test hands are being run.')

    for i in range(NUM_HANDS):
        comboSucceed = False #worth 9
        waterfrontSucceed = False#worth 4.5
        azathotSucceeded = False #worth 3

        if can_combo():
            comboSuccess += 1
            comboSucceed = True

            if debug:
                for card in deck[0:8]:
                    print(card.name)
                print()
            if contains_waterfront():
                waterfrontSucceed = True
                waterfrontSuccess += 1

            for testHand in list(itertools.permutations(hand)):#order matters so we check all possibilities
                fourCardHand = can_make_azathot_helper(list(testHand))
                if can_make_azathot(fourCardHand):
                    if debug:
                        for card in testHand:
                            print(card.name, 'SUCCEEDED AZATHOT', grave[0].name)
                        print()
                    azathotSuccess += 1
                    azathotSucceeded = True
                    break

            if not azathotSucceeded:
                if debug:
                    for card in hand:
                        print(card.name, 'FAILED AZATHOT')
                    print()
        else:
            if debug:
                print('This hand failed to combo.')
                for card in hand:
                    print(card.name)
                print()
                    
        #figure out which case it belongs to
        if not comboSucceed:
            case[1] += 1
        elif not waterfrontSucceed and not azathotSucceeded:
            case[2] += 1
        elif not waterfrontSucceed and azathotSucceeded:
            case[3] += 1
        elif waterfrontSucceed and not azathotSucceeded:
            case[4] += 1
        elif waterfrontSucceed and azathotSucceeded:
            case[5] += 1

        reset(originalDeck)


    print(comboSuccess/NUM_HANDS, 'combo percentage')
    print(waterfrontSuccess/NUM_HANDS, 'waterfront percentage')
    print(azathotSuccess/NUM_HANDS, 'azathot percentage')
    print()

    print(case[1]/NUM_HANDS, 'of hands worth 0')
    print(case[2]/NUM_HANDS, 'of hands worth', CASE2)
    print(case[3]/NUM_HANDS, 'of hands worth', CASE3)
    print(case[4]/NUM_HANDS, 'of hands worth', CASE4)
    print(case[5]/NUM_HANDS, 'of hands worth', CASE5)
    print()
    score = average_point_value(case)
    print(f'{deckFileName} scored', average_point_value(case))

    return score

def calculate_confidence_interval(data, alpha):
    if alpha == .01 and NUM_SAMPLE_MEANS == 201:
        tVal = 2.601
    elif alpha == .01 and NUM_SAMPLE_MEANS == 101:
        tVal = 2.626
    elif alpha == .01 and NUM_SAMPLE_MEANS == 51:
        tVal = 2.678
    elif alpha == .01 and NUM_SAMPLE_MEANS == 26:
        tVal = 2.787
    elif alpha == .01 and NUM_SAMPLE_MEANS == 10:
        tVal = 3.169
    elif alpha == .1 and NUM_SAMPLE_MEANS == 101:
        tVal = 1.660 
    
    avg = sum(data)/len(data)
    sqrdError = 0
    for num in data:
        sqrdError += (num - avg) * (num - avg)

    variance = sqrdError/len(data)
    stdDev = math.sqrt(variance)
    
    return (avg, avg - tVal * stdDev, avg + tVal * stdDev)


def main():
    global NUM_HANDS
    global NUM_SAMPLE_MEANS

    start = time.time()


    if len(sys.argv) == 1 or sys.argv[1] == 'help':
        print('USAGE MESSAGE')
        print('python simulate.py file [path/to/file] [# of test hands]')

    elif sys.argv[1] == 'file':
        if len(sys.argv) == 2: #default file/params
            run_simulation(DECK_FILE_NAME)
        elif len(sys.argv) == 3: #custom file/default params
            run_simulation(sys.argv[2])
        elif len(sys.argv) == 4: #custom file/custom params
            NUM_HANDS = int(sys.argv[3])
            run_simulation(sys.argv[2])


    elif sys.argv[1] == 'optimize-winners':
        for i in range(100):
            means = []
            for filename, score in ALL_DECK_NAMES:
                scoreList = []
                for i in range(NUM_SAMPLE_MEANS):
                    scoreList.append(run_simulation(filename))
                mean, lowerBound, upperBound = calculate_confidence_interval(scoreList, .01)
                means.append((filename, mean))

            means = sorted(means, key = lambda x : x[1])
            for i in range(len(means)):
                winners[means[i][0]] += i

        print(sorted(winners.items(), key = lambda x : -x[1]))
    
    elif sys.argv[1] == 'optimize-two':
        deck1 = './ten/ten4.ygo'
        deck2 = './nine/nine5.ygo'
        winners = defaultdict(int)
        deck1Scores = []
        deck2Scores = []

        for i in range(NUM_SAMPLE_MEANS):
            deck1Scores.append(run_simulation(deck1))

        for i in range(NUM_SAMPLE_MEANS):
            deck2Scores.append(run_simulation(deck2))

        mean1, lowerBound1, upperBound1 = calculate_confidence_interval(deck1Scores, .1)
        mean2, lowerBound2, upperBound2 = calculate_confidence_interval(deck2Scores, .1)

        print('Mean for', deck1, 'was', mean1, 'lower bound', lowerBound1, 'upper bound', upperBound1)
        print('Mean for', deck2, 'was', mean2, 'lower bound', lowerBound2, 'upper bound', upperBound2)

        print('Separation was', lowerBound1 - upperBound2)

                
            
    end = time.time()
    print('Your simulation took', end-start, 'seconds')
            




if __name__ == '__main__':
    main()
