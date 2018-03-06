#!/bin/python
# -*- coding: utf-8 -*- 
#import roomai.common
import copy
import functools
point_str_to_rank           = {'1':0, '2':1, '3':2, '4':3,  '5':4,  '6':5,  '7':6,  '8':7,\
                               '9':8}
point_rank_to_str           = {0:'1', 1:'2', 2:'3', 3:'4', 4:'5',  5:'6',  6:'7',   7:'8',\
                                8:'9'}
'''
筒，条，万，东西南北风，中，发，白
'''
suit_str_to_rank            = {'Dot':0, 'Bamboo':1, 'Character':2, 'EastWind':3, 'SouthWind':4, \
                                'WestWind':5, 'NorthWind':6, 'Red':7, 'Green':8,\
                                'WhiteDragon':9}
suit_rank_to_str            = {0:'Dot', 1:'Bamboo', 2: 'Character', 3:'EastWind', 4:'SouthWind', \
                                5:'WestWind', 6:'NorthWind', 7:'Red', 8:'Green', \
                                9:'WhiteDragon'}


class StateSpace:
    """
    """
    drawStage       = 1
    discardStage    = 2

class MahjongCard(object):
    """docstring for MahjongCard"""
    def __init__(self, point, suit = None):
        point1 = 0
        suit1  = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_rank[kv[0]]
            suit1  = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1  = suit
            if isinstance(suit, str):
                #print suit
                suit1 = suit_str_to_rank[suit]

        self.__point_str__  = point_rank_to_str[point1]
        self.__suit_str__   = suit_rank_to_str[suit1]
        self.__point_rank__ = point1
        self.__suit_rank__  = suit1
        self.__key__        = "%s_%s"%(self.__point_str__, self.__suit_str__)
        #self.__win_pattern__ = []
    def __get_point_str__(self):
        return self.__point_str__
    point = property(__get_point_str__, doc="The point of the mahjong card")

    def __get_suit_str__(self):
        return self.__suit_str__
    suit = property(__get_suit_str__, doc="The suit of the mahjong card")

    def __get_point_rank__(self):
        return self.__point_rank__
    point_rank = property(__get_point_rank__, doc="The point rank of the mahjong card")

    def __get_suit_rank__(self):
        return self.__suit_rank__
    suit_rank = property(__get_suit_rank__, doc="The suit rank of the mahjong card")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the mahjong card")

    # @classmethod
    # def istriple(cls,mahjongcard1, mahjongcard2, mahjongcard3):
    #     '''
    #         Compare three mahjong cards with their points and suit is same

    #         :param pokercard1: 
    #         :param pokercard2:
    #         :param pokercard3: 
    #         :return: the same true others false

    #     '''
    #     st1 = pokercard1.get_suit_rank()
    #     st2 = pokercard2.get_suit_rank()
    #     st3 = pokercard3.get_suit_rank()

    #     pr1 = pokercard1.get_point_rank()
    #     pr2 = pokercard2.get_point_rank()
    #     pr3 = pokercard3.get_point_rank()

    #     if st1 == st2 and st2 == st3  and pr1 == pr2 and pr2 == pr3:
    #         return True
    #     else:
    #         return False
    @classmethod
    def isPair(cls, mahjongcard1, mahjongcard2):
        '''
            Compare two mahjong cards with their points and suit is same

            :param mahjongcard1: 
            :param mahjongcard2: 
            :return: the same true others false

        '''
        key1 = mahjongcard1.__key__
        key2 = mahjongcard2.__key__

        if key1 == key2:
            return True
        else:
            return False
    @classmethod
    def isTriple(cls,mahjongcard1, mahjongcard2, mahjongcard3):
        '''
            Compare three mahjong cards with their points and suit is same

            :param mahjongcard1: 
            :param mahjongcard2:
            :param mahjongcard3: 
            :return: the same true others false

        '''
        key1 = mahjongcard1.__key__
        key2 = mahjongcard2.__key__
        key3 = mahjongcard3.__key__

        if key1 == key2 == key3:
            return True
        else:
            return False
    @classmethod
    def isQuadruple(cls,mahjongcard1, mahjongcard2, mahjongcard3, mahjongcard4):
        '''
            Compare three mahjong cards with their points and suit is same

            :param mahjongcard1: 
            :param mahjongcard2:
            :param mahjongcard3:
            :param mahjongcard3: 
            :return: the same true others false

        '''
        key1 = mahjongcard1.__key__
        key2 = mahjongcard2.__key__
        key3 = mahjongcard3.__key__
        key4 = mahjongcard4.__key__

        if key1 == key2 == key3 == key4:
            return True
        else:
            return False 
    @classmethod
    def isSequence(cls,mahjongcard1, mahjongcard2, mahjongcard3):
        '''
            Compare three mahjong cards with their points and suit is sequence
            Notice Thr sequence is mahjongcard1-mahjongcard2-mahjongcard3
            :param mahjongcard1: 
            :param mahjongcard2:
            :param mahjongcard3:
            :return: the sequence true others false

        '''
        suit1 = mahjongcard1.__suit_rank__
        suit2 = mahjongcard2.__suit_rank__
        suit3 = mahjongcard3.__suit_rank__

        pr1 = mahjongcard1.__point_rank__
        pr2 = mahjongcard2.__point_rank__
        pr3 = mahjongcard3.__point_rank__

        if suit1 == suit2 == suit3 and pr2 - pr1 == pr3 - pr2 == 1 :
            return True
        else:
            False
    @classmethod
    def compare(cls,mahjongcard1,mahjongcard2):
        '''
        Compare two poker cards with their point ranks and suit ranks.
        The poker card with the higher point rank has the higher rank.
        With the same point rank, the poker card with the higher suit rank has the higher rank.
        
        :param mahjongcard1: 
        :param mahjongcard2: 
        :return: A number, which is >0 when the poker card1 has the higher rank than the poker card2, =0 when their share the same rank, <0 when the poker card1 has the lower rank than the poker card2
        
        '''
        #key = 0
        #for i in range(10):
        #    key = key + (mahjongcard1.suit_rank - mahjongcard2.suit_rank)
        return  (mahjongcard1.__suit_rank__ - mahjongcard2.__suit_rank__) * 10  + (mahjongcard1.__point_rank__ - mahjongcard1.__point_rank__)
        #pr1 = mahjongcard1.suit
        #pr2 = mahjongcard2.suit

        #value1 = mahjongcard1.suit_rank  * 100 + mahjongcard1.point_rank
#
        #value2 = mahjongcard2.suit_rank  * 100 + mahjongcard1.point_rank

        #return value1 - value2
        #if pr1 == pr2:
        #    return mahjongcard1.point_rank - mahjongcard2.point_rank
        #else:
        #    return mahjongcard1.suit_rank - mahjongcard2.suit_rank
    @classmethod
    def isWin(cls,mahjongcards):
        # 
        # pair win 
        #
        global win_pattern
        #print len(win_pattern)

        key = ",".join([each.__key__ for each in mahjongcards])
        #print key
        #print win_pattern[0]
        #assert 0
        #return False
        if key in win_pattern:
            return True
        else:
            return False
            
    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = MahjongCard(self.key)
        newinstance.__point_str__  = self.__point_str__
        newinstance.__suit_str__   = self.__suit_str__
        newinstance.__suit_rank__  = self.__suit_rank__
        newinstance.__point_rank__ = self.__point_rank__
        return newinstance

AllMahjongCards = dict()
for i in range(0,4):
    for point in point_str_to_rank:
        for suit in suit_str_to_rank:
            if suit not in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
                AllMahjongCards["%s_%s" %(point,suit)] = MahjongCard("%s_%s" %(point,suit))
    for suit in ['EastWind','SouthWind','WestWind','NorthWind','Red','Green','WhiteDragon']:
        point = "1"
        AllMahjongCards["%s_%s" %(point,suit)] = MahjongCard("%s_%s" %(point,suit))



win_pattern = {}
if len(win_pattern) == 0:
    #fwrite = open("/Users/jichao/Desktop/RoomAI/roomai/mahjong/result_sort.txt","w")
    #fopen = open("result.txt","r")
    #for each in open("D:/RoomAI/roomai/mahjong/result.txt","r"):
    for each in open("/Users/jichao/Desktop/RoomAI/roomai/mahjong/result_sort.txt","r"):
        #cards = [MahjongCard(each_card.split("_")[1],each_card.split("_")[0]) for each_card in each.strip().split(",")]
        #print cards[0].key
        #cards.sort(key = functools.cmp_to_key(MahjongCard.compare))
        
        #card_pattern = ",".join([card.key for card in cards])
        #print card_pattern
        #assert 0
        #win_pattern.append(card_pattern)
        #fwrite.write(card_pattern + "\n")
        #win_pattern.append(each.strip())
        win_pattern[each] = 0
    #fwrite.close()
    #print len(win_pattern)
    #print win_pattern[0]
    #assert 0




    
