import ygocard 
import cardnames as cn

allowedCards = {cn.CRU_MAX_STR,
                cn.CRU_ARB_STR,
                cn.CRU_DRA_STR,
                cn.CRU_LEO_STR,
                cn.CRU_REC_STR,
                cn.THRASHER_STR,
                cn.ROTA_STR, 
                cn.DESTRUDO_STR,
                cn.GAMACIEL_STR,
                cn.REDMD_STR,
                cn.QUICK_STR,
                cn.BLACK_DRA_STR,
                cn.WHITE_DRA_STR, 
                cn.RANRYU_STR, 
                cn.ROKKET_STR,
                cn.WATERFRONT_STR,
                cn.TERRA_STR, 
                cn.REBORN_STR,
                cn.WLG_STR, 
                cn.WLS_STR, 
                cn.JIGABYTE_STR,
                cn.INARI_STR, 
                cn.NEFARIOUS_STR,
                cn.SET_ROTATION_STR,
                cn.RAVINE_STR}

def deck_from_file(file):
    deck = []
    try:
        for line in file:
            data = line.rstrip().split(';')
            if data[0] == 'm':
                data[2] = data[2].upper()
                assert data[2] in allowedCards
                for i in range(int(data[1])):
                    deck.append(ygocard.MonsterCard(*data[2:]))

            elif data[0] == 's':
                data[2] = data[2].upper()
                assert data[2] in allowedCards
                for i in range(int(data[1])):
                    deck.append(ygocard.SpellCard(*data[2:]))

            elif data[0] == 't':
                data[2] = data[2].upper()
                assert data[2] in allowedCards
                for i in range(int(data[1])):
                    deck.append(ygocard.TrapCard(*data[2:]))
            elif data[0] == 'b': #blank
                for i in range(int(data[1])):
                    deck.append(ygocard.Blank())
            else:#igore
                #print('ignored some cards')
                pass
    except AssertionError:
        print(f'{data[2]} is not a supported card name.')
        exit()

    return deck


def main():
    with open('CG.ygo') as file:
        print(len(deck_from_file(file)))


if __name__ == '__main__':
    main()
