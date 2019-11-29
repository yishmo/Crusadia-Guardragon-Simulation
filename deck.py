import card

def deck_from_file(file):
    deck = []
    for line in file:
        data = line.rstrip().split(';')
        if data[0] == 'm':
            for i in range(int(data[1])):
                deck.append(card.MonsterCard(*data[2:]))

        elif data[0] == 's':
            for i in range(int(data[1])):
                deck.append(card.SpellCard(*data[2:]))

        elif data[0] == 't':
            for i in range(int(data[1])):
                deck.append(card.TrapCard(*data[2:]))
        else: #blank
            for i in range(int(data[1])):
                deck.append(card.Blank())


    return deck


def main():
    with open('CG.ygo') as file:
        print(len(deck_from_file(file)))


if __name__ == '__main__':
    main()
