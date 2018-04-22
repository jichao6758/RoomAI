#!/bin/python
#coding=utf8

import random
import copy
#from roomai.common import *
#import roomai
import sys
#sys.path.append("d:/RoomAI/")
sys.path.append("/Users/jichao/Documents/RoomAi/RoomAI/")
import roomai.common
import logging
import time
from roomai.common import Info
from roomai.mahjong import MahjongCard
from MahjongInfo import *
from MahjongAction import *
from MahjongUtil import *
import functools

step = 0
class MahjongEnv(roomai.common.AbstractEnv):

    @classmethod
    def __check_initialization_configuration__(cls, env):
        if env.__params__["dealer_id"] > 4:
            raise ValueError("env.dealer_id must be less 4, now env.dealer_id = %d" %(env.dealer_id))
        if env.__params__["num_players"] != 4:
            raise ValueError("env.num_players must be 4, now env.num_players = %d" % (env.num_players))
        return True

    # def __init__(self):
        
    #     self.num_players    = 4 
    #     self.dealer_id      = int(random.random() * self.num_players)
    # Before init, you need set the num_players, dealer_id
    #@override
    def init(self,params = dict()):
        '''Initialize
        
        Initialize the TexasHoldem game environment with the initialization params.
       
        Keyword Arguments:
            params {[type]} -- [description] (default: {dict()})
        '''
        
        self.logger         = roomai.get_logger()

        self.__params__ = {}

        if "dealer_id" in params:
            self.__params__["dealer_id"] = params["dealer_id"]
        else:
            self.__params__["dealer_id"] = int(random.random() * params["num_players"])

        self.__params__["num_players"] = params["num_players"]
        self.__params__["allcards"] = []
        if "allcards" not in params:
            for y in xrange(9):
                for z in xrange(3):
                    self.__params__["allcards"].append(MahjongCard(y,z))
            for m in range(4,9):
                self.__params__["allcards"].append(MahjongCard(0,m))

            for i in range(0,2):
                self.__params__["allcards"]  = self.__params__["allcards"] + self.__params__["allcards"]
        else:
            self.__params__["allcards"] = params["allcards"]
        # print [each.key for each in self.__params__["allcards"]]
        # assert 0
        #
        #print ",".join(["%s_%s" %(str(each),each.key) for each in self.__params__["allcards"]])

        #assert 0
        random.shuffle(self.__params__["allcards"])
        #print self.__params__["allcards"]
        if "record_history" in params:
            self.__params__["record_history"] = params["record_history"]
        else:
            self.__params__["record_history"] = False

        self.__check_initialization_configuration__(self)
        # allcards = []

        ## public info 
        self.public_state           = MahjongPublicState()
        self.public_state.__num_players__          = self.__params__["num_players"]
        self.public_state.__dealer_id__            = self.__params__["dealer_id"]
        self.public_state.__turn__                 = self.__params__["dealer_id"]
        self.public_state.__previous_id__          = None
        self.public_state.__previous_action__      = None
        self.public_state.__remaining_card_num__   = len(self.__params__["allcards"])
        self.public_state.__out_of_card__          = None
        self.public_state.__action_list__          = None
        self.public_state.__discard_player__       = None
        self.public_state.__discard__              = None
        self.public_state.__is_terminal__          = False
        self.public_state.__who_is_win__           = -1
        ## private info
        self.private_state              = MahjongPrivateState()
        self.private_state.__keep_cards__           = self.__params__["allcards"][self.__params__["num_players"]*13 + 1:]
 
        ## person info
        self.person_states          = [MahjongPersonState() for i in range(self.__params__["num_players"])]
        #person                         = self.person_states
        hand_cards       = []
        for i in xrange(self.__params__["num_players"]):
            self.person_states[i].__id__ = i
            self.person_states[i].__hand_cards__ = self.__params__["allcards"][i*13:(i+1)*13]#.sort(MahjongCard.compare)
            #person[i].__hand_cards__ = self.__params__["allcards"][i*12:(i+1)*12]#.sort(MahjongCard.compare)
            if i == self.__params__["dealer_id"]:
                self.person_states[i].__hand_cards__.append(self.__params__["allcards"][self.__params__["num_players"]*13])
 
            self.person_states[i].__hand_cards__.sort(key = functools.cmp_to_key(MahjongCard.compare))
        self.person_states[self.public_state.turn].__available_actions__ = self.available_actions(self.public_state,self.person_states[self.public_state.turn])
        self.__gen_history__()
        infos = self.__gen_infos__()
        if self.logger.level <= logging.DEBUG:
                self.logger.debug("TexasHoldemEnv.init: num_players = %d, dealer_id = %d, chip = %d, big_blind_bet = %d"%(\
                    self.public_state.num_players,\
                    self.public_state.dealer_id,\
                    self.public_state.chips[0],\
                    self.public_state.big_blind_bet
                ))

        return infos, self.public_state, self.person_states, self.private_state
    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        public  = self.public_state
        person = self.person_states
        private = self.private_state
        #global step
        #step = step + 1
        #print "###%s" %step

        """[summary]
        动作为胡,直接game_over,计算得分
        """
        if action.effective == True and action.option == MahjongAction.Win:
            public.__previous_id__      = public.__turn__
            public.__previous_action__  = action
            public.__is_terminal__      = True
            public.__scores__           = self.__compute_scores__()
            public.__who_is_win__       = public.__turn__
            self.__gen_history__()
            return self.__gen_infos__(),public,person,private
        
        """[summary]
        动作为吃,或者碰
        """
        if action.effective == True: #and (action.option == MahjongAction.Pong or action.option == MahjongAction.Chow):
            public.__previous_id__      = public.__turn__
            public.__previous_action__  = action           
            action_cards = action.__card_list__
            to_del = {}
            for each in action_cards:
                if each not in to_del:
                    to_del[each] = 1
                else:
                    to_del[each] = to_del[each] + 1
            if action.option != action.Discard:
                if public.__discard_card__ in to_del:
                    to_del[public.__discard_card__] = to_del[public.__discard_card__] - 1
                person[public.__turn__].__discard__ = person[public.__turn__].__discard__ + action_cards
            person[public.__turn__].__del_card__(to_del)
            '''[summary]
            
            将碰的牌记录到public_state
            '''
            if action.option in (MahjongAction.Pong,MahjongAction.Chow,MahjongAction.Kong,MahjongAction.ConKong):
                #print action.__card__
                #assert 0
                #person[public.__turn__].____out_of_hand_cards__.append(action.__card__)
                person[public.__turn__].__out_of_hand_cards__ = person[public.__turn__].__out_of_hand_cards__ +  action.__card_list__
                # print len(person[public.__turn__].__out_of_hand_cards__)
                # print person[public.__turn__].__out_of_hand_cards__
                # print len(person[public.__turn__].__hand_cards__)
                # assert 0
                # 如果动作是非杠或者暗杠
                if action.option != MahjongAction.ConKong:
                    public.__players_action__.append((action.option,public.__discard_player__,public.__turn__,action.__card__))
                else:
                    public.__players_conkong__.append(public.__turn__)
                    person[public.__turn__].__conkong__.append(action.__card__)
                if  action.option in (MahjongAction.Kong,MahjongAction.ConKong):
                    if len(private.__keep_cards__) > 0:
                        person[public.__turn__].__add_card__(private.__keep_cards__.pop())
                    else:
                        public.__is_terminal__ = True
                        public.__scores__           = self.__compute_scores__()
                #person[public.__turn__].__discard__           = []
                public.__turn__                               = public.__turn__
                person[public.__turn__].__available_actions__ = self.available_actions(public,person[public.__turn__])
                #
                #print person[public.__turn__].__available_actions__
                self.__gen_history__()
                return self.__gen_infos__(),public,person,private
            if action.option == MahjongAction.Discard:
                public.__discard_player__ = public.__turn__
                public.__discard_card__   = action.__card_list__[0]
        #assert 0
        #判断是不是有人胡牌
        i = (public.__turn__ + 1) % self.__params__["num_players"]
        # print action.option
        # print action.__card__
        # print public.__discard_player__
        # print "******"
        while (i != public.__discard_player__ and public.__discard_player__ is not None): 
            # print  "player: %d" %i
            # print len(person[i].__hand_cards__)
            # print "end"
            available_actions = self.available_actions_win(public,person[i])
            if len(available_actions) != 0:
                public.__previous_id__     = public.__turn__
                public.__previous_action__ = action
                person[i].__available_actions__ = available_actions
                public.__turn__ = i
                self.__gen_history__()
                return self.__gen_infos__(),public,person,private
            i = (i + 1) % self.__params__["num_players"]
        #
        #判断是不是有人碰
        i = (public.__turn__ + 1) % self.__params__["num_players"]
        while (i != public.__discard_player__ and public.__discard_player__ is not None):
            available_actions = self.available_actions_kong(public,person[i])
            if len(available_actions) != 0:
                public.__previous_id__     = public.__turn__
                public.__previous_action__ = action
                person[i].__available_actions__ = available_actions
                public.__turn__ = i
                self.__gen_history__()
                return self.__gen_infos__(),public,person,private
            i = (i + 1) % self.__params__["num_players"]
        public.__previous_id__ = public.__turn__
        public.__previous_action__ = action
        if public.__discard_player__ is not None:
            public.__turn__ = (public.__discard_player__ + 1) % self.__params__["num_players"]
        else:
            public.__turn__ = (public.__turn__ + 1) % self.__params__["num_players"]

        available_actions = self.available_actions_chow(public,person[public.__turn__])
        if len(available_actions) == 0:
            if len(private.__keep_cards__) != 0:
                person[public.__turn__].__add_card__(private.__keep_cards__.pop())
                #print "hand_cards"
                #print person[public.__turn__].__hand_cards__
                #print len(person[public.__turn__].__hand_cards__)
                available_actions = self.available_actions(public,person[public.__turn__])
                #print "action"
                #for each in available_actions:
                #    print available_actions[each].__card_list__
            else:
                public.__is_terminal__ = True
                public.__scores__           = self.__compute_scores__()
        person[public.__turn__].__available_actions__ = available_actions
        self.__gen_history__()
        return self.__gen_infos__(),public,person,private
            
    
            
    @classmethod
    def available_actions(cls, public_state, person_state):
        '''
        Generate all valid actions given the public state and the person state
        :param public_state:
        :parre person_state:
        :return:all valid actions
        '''
        public  = public_state
        person  = person_state
        turn    = public.turn
        key_actions = dict()
        #available_actions = {}
        cards = person.__hand_cards__ #+ person.__out_of_hand_cards__

        cards.sort(key = functools.cmp_to_key(MahjongCard.compare))
        # if (len(cards) != 14):
        #     print len(person.__hand_cards__)
        #     print len(person.__out_of_hand_cards__)
        #     assert 0
        if MahjongCard.isWin(cards) == True:
            key = "%s_%s_%s" %(MahjongAction.Win,0,":".join([each.key for each in cards]))
            key_actions[key] = MahjongAction.lookup(key,cards)
        for i in range(len(person.hand_cards)):
             key = "%s_%s_%s" %(MahjongAction.Discard,0,person.hand_cards[i].key)
             key_actions[key] = MahjongAction.lookup(key,[person.hand_cards[i]])

        i = 0
        while i < len(person.hand_cards) - 3:
            if MahjongCard.isQuadruple(person.hand_cards[i],person.hand_cards[i + 1],person.hand_cards[i + 2],person.hand_cards[i + 3]) == True:
                cards_list = [person.hand_cards[i],person.hand_cards[i + 1],person.hand_cards[i + 2],person.hand_cards[i + 3]]
                key = "%s_%s_%s" %(MahjongAction.ConKong,0,":".join([each.key for each in cards_list]))
                key_actions[key] = MahjongAction.lookup(key,cards_list)
                i = i + 4    
            else:
                i = i + 1
        return key_actions

    def available_actions_kong(cls,public_state,person_state):
        public  = public_state
        person = person_state
        turn    = public.turn
        key_actions = dict()
        #available_actions = {}
        discard = public.__discard_card__
        isExistChow = False
        for i in range(len(person.hand_cards) - 2):
            if person.hand_cards[i].key == discard.key:
                if MahjongCard.isQuadruple(discard,person.hand_cards[i],person.hand_cards[i + 1],person.hand_cards[i + 2]) == True:
                    cards_list = [discard,person.hand_cards[i],person.hand_cards[i + 1],person.hand_cards[i + 2]]
                    key = "%s_%s_%s" %(MahjongAction.Kong,turn,":".join([each.key for each in cards_list]))
                    key_actions[key] = MahjongAction.lookup(key,cards_list)
                    return key_actions
                else:
                    return key_actions

        return key_actions
    def available_actions_chow(cls, public_state, person_state):
        public  = public_state
        person  = person_state
        turn    = public.turn
        key_actions = dict()
        #available_actions = {}
        discard = public.__discard_card__
        isExistChow = False
        if discard is None:
            return key_actions
        for i in range(len(person.hand_cards) - 1):
            if MahjongCard.isSequence(discard,person.hand_cards[i],person.hand_cards[i + 1]) == True:
                cards_list = [discard,person.hand_cards[i],person.hand_cards[i + 1]]
                isExistChow = True
                key = "%s_%s_%s" %(MahjongAction.Chow,turn,":".join([each.key for each in cards_list]))
                key_actions[key] = MahjongAction.lookup(key,cards_list)
                #print "in"
                #print key
                #print "out"
                isExistChow = False
            # elif MahjongCard.isSequence(person.hand_cards[i],discard,person.hand_cards[i + 1]) == True:
            #     isExistChow = True
            # elif MahjongCard.isSequence(person.hand_cards[i],person.hand_cards[i + 1], discard) == True:
            #     isExistChow = True
                #key_actions[MahjongAction.Chow].append((person.hand_cards[i],person.hand_cards[i + 1]))
        return key_actions

    def available_actions_win(cls,public_state,person_state):
        public  = public_state
        person = person_state
        turn    = public.turn
        key_actions = dict()
        #available_actions = {}
        discard = public.__discard_card__
        cards = []
        isInsert = False
        cards = person.__hand_cards__ #+ person.__out_of_hand_cards__

        #print person.__discard__
        cards.append(discard)
        cards.sort(key = functools.cmp_to_key(MahjongCard.compare))
        # if (len(cards) != 14):
        #     print len(person.__hand_cards__)
        #     print len(person.__out_of_hand_cards__)
        #     print public.__discard_card__.key
        #     assert 0
        #for each in person.hand_cards:
        #    if MahjongCard.compare(each,discard) < 0 or isInsert == True:
        #        cards.append(each)
        #    elif isInsert == False:
        #        cards.append(discard)
        #        cards.append(each)
        #        isInsert == True
        if MahjongCard.isWin(cards) == True:
            key = "%s_%s_%s" %(MahjongAction.Win,turn,":".join([each.key for each in cards]))
            key_actions[key] = MahjongAction.lookup(key,cards)
        return key_actions
    @classmethod
    def compete(cls, env, players):
        '''   
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: the winer
        '''
        num_players = len(players)
        global AllMahjongCards
        #print AllMahjongCards
        allcards = []

        for each in AllMahjongCards:
            allcards.append(AllMahjongCards[each])
        for i in range(2):
            allcards = allcards + allcards
        #print len(allcards)
        #
        infos, public, person, private = env.init({"num_players":num_players,"allcards":allcards})
        #assert 0
        for i in range(public.num_players):
            players[i].receive_info(infos[i])

        while public.is_terminal == False:
            turn = public.turn
            action = players[turn].take_action()

            #print action.key
            #assert 0
            infos,public,persons,private = env.forward(action)
             
            for i in range(env.__params__["num_players"]):
                players[i].receive_info(infos[i])
        print public.scores
        #print time.clock()
        return public.scores

    def __compute_scores__(self):
        scores = [-1 for i in range(self.__params__["num_players"])]
        if self.public_state.__who_is_win__ != -1:
            scores[self.public_state.__who_is_win__]  = 100
        return scores
     
if __name__ == '__main__':
    abc= MahjongEnv()
