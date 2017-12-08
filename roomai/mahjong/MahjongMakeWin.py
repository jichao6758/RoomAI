from MahjongUtil import MahjongCard

suit_list = ['Dot','Bamboo','Character','EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']
point_list = ['1','2','3','4','5','6','7','8','9']
if __name__ == '__main__':
    mahjong_map = {}
    for suit in suit_list:
        if suit not in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
            for point in point_list:
                mahjong_map[suit + "_" + point] = 0
        else:
            mahjong_map[suit + "_" + point] = 0
    print mahjong_map

    #abc = dict(suit_map)
    #all_cards = {}
    # for x in xrange(4):
    #         for y in xrange(9):
    #             for z in xrange(3):
    #                 all_cards.append(MahjongCard(y,z))
    #         for m in range(3,10):
    #             all_cards.append(MahjongCard(0,m))
    # print len(all_cards)
