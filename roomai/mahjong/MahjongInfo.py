#!/bin/python
import roomai.common
from roomai.mahjong import MahjongCard
class MahjongPublicState(roomai.common.AbstractPublicState):
    """[summary]
    
    [description]
    
    Extends:
        roomai.common.AbstractPublicState
    
    Variables:
        AllMahjongActions {[type]} -- [description]
    """
    def __init__(self):
        '''[summary]
        
        ''' 
        self.__num_players            = None    # palyer_num
        self.__dealer_id__            = None    # who is dealer
        self.__turn__                 = None    # next turn
        self.__previous_id__          = None    # previous_id
        self.__previous_action__      = None    # previous_action
        self.__remaining_card_num__   = None    # remaining_car_num
        self.__out_of_card__          = None    # out of card
        self.__win_by_discard__       = None    # the id of who discard 
        @property
        def dealer_id(self):
            return self.__dealer_id

        @property
        def num_players(self):
            return self.__num_players

        @property
        def remaining_card_num(self):
            return self.__remaining_card_num

        @property
        def previous_id(self):
            return self.__previous_id

        @property
        def previous_action(self):
            return self.__previous_action

        '''[summary]
        
        state of players
        '''
        
        

        self.__players_cards_num__    = None   # the list of number of players` remaining cards 
        self.__discard_player__       = None   # the number of players who is the lastest discard
        self.__players_chow__         = None 
        self.__players_pong__         = None
        self.__players_kong__         = None
        self.__players_conkong__      = None

        @property
        def players_cards_num(self):
            return self.__players_cards_num

        @property
        def players_ready_hand(self):
            return self.__players_ready_hand

        @property
        def players_chow(self):
            return self.__players_chow

        @property
        def players_pong(self):
            return self.__players_pong

        @property 
        def players_kong(self):
            return self.__players_kong

        @property
        def players_conkong(self):
            return self.__players_conkong

    def __deepcopy__(self, memodict={}):
        '''[summary]
        
        [description]
        
        Keyword Arguments:
            memodict {dict} -- [description] (default: {{}})
        '''  
        copyinstance                      = MahjongPublicState()
        copyinstance.dealer_id            = self.dealer_id
        copyinstance.num_players          = self.num_players
        copyinstance.remaining_card_num   = self.remaining_card_num
        copyinstance.who_discard          = self.who_discard
        copyinstance.discard_state        = self.discard_state
        if self.players_cards_num is None:
            copyinstance.players_cards_num = None
        else:
            copyinstance.players_cards_num = [self.players_cards_num[i] for i in xrange(len(self.players_cards_num))]
        if self.players_ready_hand is None:
            copyinstance.players_ready_hand = None
        else:
            copyinstance.players_ready_hand = [self.players_ready_hand[i] for i in xrange(len(self.players_ready_hand))]
        if self.players_chow is None:
            copyinstance.players_chow = None
        else:
            copyinstance.players_chow = [(self.players_chow[i][0],self.players_chow[i][1].__deepcopy__(),self.players_chow[i][2].__deepcopy__(),self.players_chow[i][3].__deepcopy__()) for i in xrange(len(self.players_pong))]
        if self.players_pong is None:
            copyinstance.players_pong = None
        else:
            copyinstance.players_pong = [(self.players_pong[i][0],self.players_pong[i][1].__deepcopy__()) for i in xrange(len(self.players_pong))]
        if self.players_kong is None:
            copyinstance.players_kong = None:
        else:
            copyinstance.players_kong = [(self.players_kong[i][0],self.players_kong[i][1].__deepcopy__()) for i in xrange(len(self.players_pong))]
        if self.players_conkong is None:
            copyinstance.players_conkong = None
        else:
            copyinstance.players_conkong = [self.players_conkong[i] for i in xrange(len(self.players_conkong))]

class MahjongPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        super(MahjongPrivateState,self).__init__()
        self.__keep_cards__   = []

        @property
    def keep_cards(self):
        return tuple(self.__keep_cards__)

    def __deepcopy__(self, memodict={}):

        copy = new MahjongPrivateState
        if self.keep_cards == None:
            copy.keep_cards = None
        else:
            copy.keep_cards = [self.keep_cards[i].__deepcopy__() for i in xrange(len(self.keep_cards))]

        return copy 
class MahjongPersonState(roomai.common.AbstractPersonState):
    """
    """
    

    def __init__(self):
        super(MahjongPersonState,self).__init__()
        self.__id__                 =    0
        self.__hand_cards__         =    []
        self.__available_actions__  =    dict() 
        self.__show_cards__         =    dict()
        self.__discard__            =    []

    @property
    def id(self):
        return tuple(self.__id)

    @property    
    def hand_cards(self):
        return tuple(self.__hand_cards__)

    def __add_card__(self,c):
        self.__hand_cards__.append(c)

        for j in range(len(self.__hand_cards__)-1,0,-1):
            if MahjongCard.compare(self.__hand_cards__[j - 1], self.__hand_cards__[j]) > 0:
                tmp = self.__hand_cards__[j]
                self.__hand_cards__[j] = self.__hand_cards__[j-1]
                self.__hand_cards__[j-1] = tmp
            else:
                break


    def __del_card__(self,c):
        tmp = self.__hand_cards__
        self.__hand_cards__ = []
        for i in range(len(tmp)):
            if c.key == tmp[i].key:
                continue
            self.__hand_cards__.append(tmp[i])


    def __deepcopy__(self, memodict={}):
        copyinstance    = MahjongPersonState()
        copyinstance.id = self.id
        if self.hand_cards is not None:
            copyinstance.hand_cards = [self.hand_cards[i].__deepcopy__() for i in xrange(len(self.hand_cards))]
        else:
            copyinstance.hand_cards = None

        if self.available_actions is not None:
            copyinstance.available_actions = dict()
            for key in self.available_actions:
                copyinstance.available_actions[key] = self.available_actions[key].__deepcopy__()
        else:
            copyinstance.available_actions = None
        return copyinstance

AllCardsPattern = dict{}
#0     1           2       3           4                                    5     6
#name, StraightNum, PairNum, SameSuit, [SizeOfPair1, SizeOfPair2,..](desc), rank, cards
AllCardsPattern[""]