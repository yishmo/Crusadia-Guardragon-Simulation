import ygocard

def deck_from_file(file):
    deck = []
    for line in file:
        data = line.rstrip().split(';')
        if data[0] == 'm':
            for i in range(int(data[1])):
                deck.append(ygocard.MonsterCard(*data[2:]))

        elif data[0] == 's':
            for i in range(int(data[1])):
                deck.append(ygocard.SpellCard(*data[2:]))

        elif data[0] == 't':
            for i in range(int(data[1])):
                deck.append(ygocard.TrapCard(*data[2:]))
        elif data[0] == 'b': #blank
            for i in range(int(data[1])):
                deck.append(ygocard.Blank())
        else:#igore
            #print('ignored some cards')
            pass


    return deck


def main():
    with open('CG.ygo') as file:
        print(len(deck_from_file(file)))


if __name__ == '__main__':
    main()
