from MahjongUtil import MahjongCard
import functools
suit_list = ['Dot','Bamboo','Character','EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']
point_list = ['1','2','3','4','5','6','7','8','9']
all_list = dict()
def process_fun(card_list,start):
    global key_list
    key = key_list[start]
    #print card_list
    #print key
    # global i 
    # i = i + 1 
    #print mahjong_map
    for each_key in mahjong_map:
        if mahjong_map[each_key] > 4:
            return
            #print mahjong_map
            #assert 0
    #print card_list
    global win_card_num
    if len(card_list) == win_card_num:
        #assert 0
        #print card_list
        global all_list
        #print card_list
        cards = [MahjongCard(each) for each in card_list]
        cards.sort(key = functools.cmp_to_key(MahjongCard.compare))
        card_keys = ",".join([card.key for card in cards])
        
        if card_keys not in all_list:
            #print(card_keys)
            print card_keys
            all_list[card_keys] = 0
            #assert 0
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
        for i in range(start,len(key_list)):
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
    for each_round in range(2,17,3):
        win_card_num = each_round
        mahjong_map = {}
        for suit in suit_list:
            if suit not in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
                for point in point_list:
                    mahjong_map[point + "_" + suit] = 0
            else:
                mahjong_map["1" + "_" + suit] = 0
        card_list = []
        key_list_card = [MahjongCard(each) for each in mahjong_map]

        key_list_card.sort(key = functools.cmp_to_key(MahjongCard.compare))
        #print MahjongCard.compare(key_list_card[0],key_list_card[1])
        #print MahjongCard.compare(key_list_card[1],key_list_card[2])
        key_list = [each.key for each in key_list_card]
        #print key_list
        for start in range(len(key_list)):
            #print start
            # if win_card_num == 5:
            #     print start 
            #     print mahjong_map
            #     assert 0
            card_list.append(key_list[start])
            card_list.append(key_list[start])
            mahjong_map[key_list[start]] = mahjong_map[key_list[start]] + 2
            for i in range(len(key_list)):
                process_fun(card_list,i)
            mahjong_map[key_list[start]] = mahjong_map[key_list[start]] - 2
            card_list.pop()
            card_list.pop()

