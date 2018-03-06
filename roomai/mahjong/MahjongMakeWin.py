from MahjongUtil import MahjongCard

suit_list = ['Dot','Bamboo','Character','EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']
point_list = ['1','2','3','4','5','6','7','8','9']
i = 0
is_pair = False
all_list = dict()
def process_fun(card_list,start):
    key = mahjong_map.keys()[start]
    #print key
    global i 
    i = i + 1 
    for each_key in mahjong_map:
        if mahjong_map[each_key] > 4:
            return
            #print mahjong_map
            #assert 0
    #print card_list
    if len(card_list) == 14:
        #print card_list
        global all_list
        #print card_list
        if ",".join(card_list) not in all_list:
            print ",".join(card_list)
            all_list[",".join(card_list)] = 0
            assert 0
        return 
    if mahjong_map[key] >= 4:
        return
    '''
    if mahjong_map[key] <= 2 and is_pair == False:
        card_list.append(key)
        card_list.append(key)
        mahjong_map[key] = mahjong_map[key] + 2
        global is_pair
        is_pair = True
        for i in range(start,len(mahjong_map.keys())):
            process_fun(card_list,i)
        mahjong_map[key] = mahjong_map[key] - 2
        card_list.pop()
        card_list.pop()
    '''
    if mahjong_map[key] <= 1:
        card_list.append(key)
        card_list.append(key)
        card_list.append(key)
        mahjong_map[key] = mahjong_map[key] + 3
        for i in range(start,len(mahjong_map.keys())):
            process_fun(card_list,i)
            #print card
        mahjong_map[key] = mahjong_map[key] - 3
        card_list.pop()
        card_list.pop()
        card_list.pop()
    suit = key.split("_")[1]
    point = int(key.split("_")[0])
    #print suit
    #print point 
    #assert 0
    if suit in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
        return

    if point + 2 < 10 and mahjong_map[ "%s_" % str(point + 1) + suit ] <= 3 and mahjong_map[ "%s_" % str(point + 2) + suit ] <= 3:
        card_list.append(key)
        card_list.append( "%s_" % str(point + 1) + suit )
        card_list.append( "%s_" % str(point + 2) + suit )
        mahjong_map[key] = mahjong_map[key] + 1
        mahjong_map[ "%s_" % str(point + 1) + suit ] = mahjong_map[ "%s_" % str(point + 1) + suit ] + 1
        mahjong_map[ "%s_" % str(point + 2) + suit ] = mahjong_map[ "%s_" % str(point + 2) + suit ] + 1
        for i in range(start,len(mahjong_map.keys())):
            process_fun(card_list,i)
        mahjong_map[key] = mahjong_map[key] - 1
        mahjong_map[ "%s_" % str(point + 1) + suit ] = mahjong_map[ "%s_" % str(point + 1) + suit ] - 1
        mahjong_map[ "%s_" % str(point + 2) + suit ] = mahjong_map[ "%s_" % str(point + 2) + suit ] - 1
        card_list.pop()
        card_list.pop()
        card_list.pop()
    '''
    if point > 1 and point + 1 < 10 and mahjong_map[ "%s_" % str(point - 1) + suit ] <= 3 and mahjong_map[ "%s_" % str(point + 1) + suit ] <= 3:
        card_list.append(key)
        card_list.append( "%s_" % str(point - 1) + suit )
        card_list.append( "%s_" % str(point + 1) + suit )
        mahjong_map[key] = mahjong_map[key] + 1
        mahjong_map[ "%s_" % str(point + 1) + suit ] = mahjong_map[ "%s_" % str(point + 1) + suit ] + 1
        mahjong_map[ "%s_" % str(point - 1) + suit ] = mahjong_map[ "%s_" % str(point - 1) + suit ] + 1
        for card in mahjong_map.keys():
            process_fun(card_list,card)
        mahjong_map[key] = mahjong_map[key] - 1
        mahjong_map[ "%s_" % str(point + 1) + suit ] = mahjong_map[ "%s_" % str(point + 1) + suit ] - 1
        mahjong_map[ "%s_" % str(point - 1) + suit ] = mahjong_map[ "%s_" % str(point - 1) + suit ] - 1
        card_list.pop()
        card_list.pop()
        card_list.pop()
    if point > 2 and mahjong_map[ "%s_" % str(point - 1) + suit ] <= 3 and mahjong_map[ "%s_" % str(point - 2) + suit ] <= 3:
        card_list.append(key)
        card_list.append( "%s_" % str(point - 1) + suit )
        card_list.append( "%s_" % str(point - 2) + suit )
        mahjong_map[key] = mahjong_map[key] + 1
        mahjong_map[ "%s_" % str(point - 1) + suit ] = mahjong_map[ "%s_" % str(point - 1) + suit ] + 1
        mahjong_map[ "%s_" % str(point - 2) + suit ] = mahjong_map[ "%s_" % str(point - 2) + suit ] + 1
        for card in mahjong_map.keys():
            process_fun(card_list,card)
        mahjong_map[key] = mahjong_map[key] - 1
        mahjong_map[ "%s_" % str(point - 1) + suit ] = mahjong_map[ "%s_" % str(point - 1) + suit ] - 1
        mahjong_map[ "%s_" % str(point - 2) + suit ] = mahjong_map[ "%s_" % str(point - 2) + suit ] - 1
        card_list.pop()
        card_list.pop()
        card_list.pop()
    '''
if __name__ == '__main__':
    mahjong_map = {}
    for suit in suit_list:
        if suit not in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
            for point in point_list:
                mahjong_map[point + "_" + suit] = 0
        else:
            mahjong_map[point + "_" + suit] = 0
    #print mahjong_map
    card_list = []
    key_list = mahjong_map.keys()
    # print key_list
    # for i in range(len(key_list) - 1):
    #     print key_list[i] < key_list[i + 1]
    # assert 0 
    card_list = []
    key_list = mahjong_map.keys()
    for start in range(len(key_list)):
        card_list.append(key_list[start])
        card_list.append(key_list[start])
        mahjong_map[key_list[start]] = mahjong_map[key_list[start]] + 2
        process_fun(card_list,start)
        mahjong_map[key_list[start]] = mahjong_map[key_list[start]] - 2
        card_list.pop()
        card_list.pop()


    #abc = dict(suit_map)
    #all_cards = {}
    # for x in xrange(4):
    #         for y in xrange(9):
    #             for z in xrange(3):
    #                 all_cards.append(MahjongCard(y,z))
    #         for m in range(3,10):
    #             all_cards.append(MahjongCard(0,m))
    # print len(all_cards)
