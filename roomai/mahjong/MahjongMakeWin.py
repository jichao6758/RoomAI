from MahjongUtil import MahjongCard

suit_list = ['Dot','Bamboo','Character','EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']
point_list = ['1','2','3','4','5','6','7','8','9']

def process_fun(card_list,key):
    if len(card_list) == 13:
        all_list.append(card_list)
        return 
    if mahjong_map[key] > 4:
        return
    if mahjong_map[key] <= 1:
        card_list.append(key)
        card_list.append(key)
        card_list.append(key)
        mahjong_map[key] = mahjong_map[key] + 3
        for card in mahjong_map.key():
            process_fun(card_list,card)
    suit = key.split("_")[0]
    point = key.split("_")[1]
    if suit in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
        return
    if mahjong_map[suit + "_%s" % str(point + 1)] <= 3 and mahjong_map[suit + "_%s" % str(point + 2)] <= 3:
        card_list.append(key)
        card_list.append(suit + "_%s" % str(point + 1))
        card_list.append(suit + "_%s" % str(point + 2))
        
if __name__ == '__main__':
    mahjong_map = {}
    for suit in suit_list:
        if suit not in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
            for point in point_list:
                mahjong_map[suit + "_" + point] = 0
        else:
            mahjong_map[suit + "_" + point] = 0
    print mahjong_map
    all_list = []
    for each in mahjong_map.keys():
        cards_list = []
        cards_list.append[each]
        cards_list.append[each]
        mahjong_map[each]  = mahjong_map[each] + 2
        for each_1 in mahjong_map.keys():
            if mahjong_map[each_1] > 4:
                continue
            else:


    #abc = dict(suit_map)
    #all_cards = {}
    # for x in xrange(4):
    #         for y in xrange(9):
    #             for z in xrange(3):
    #                 all_cards.append(MahjongCard(y,z))
    #         for m in range(3,10):
    #             all_cards.append(MahjongCard(0,m))
    # print len(all_cards)
