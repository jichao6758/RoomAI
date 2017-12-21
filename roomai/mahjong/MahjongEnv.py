#!/bin/python
#coding:utf-8

import random
import copy
import roomai.common
import roomai
import logging

from roomai.common import Info
from roomai.mahjong import MahjongCard


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
            self.__params__["dealer_id"] = int(random.random() * self.num_players)

        
        self.__params__["allcards"] = []
        for x in xrange(4):
            for y in xrange(9):
                for z in xrange(3):
                    self.__params__["allcards"]append(MahjongCard(y,z))
            for m in range(4,9):
                self__params__["allcards"].append(MahjongCard(m,0))

        random.shuffle(self.__params__["allcards"])
        if "record_history" in params:
            self.__params__["record_history"] = params["record_history"]
        else:
            self.__params__["record_history"] = False

        self.__check_initialization_configuration__(self)
        # allcards = []

        ## public info 
        self.public_state           = MahjongPublicState()
        public                          = self.public_state
        public.__num_players            = self.public_state.__num_players
        public.__dealer_id__            = self.public_state.__dealer_id__
        public.__turn__                 = random.randomint(0,3)
        public.__previous_id__          = None
        public.__previous_action__      = None
        public.__remaining_card_num__   = len(self.__params__["allcards"])
        public.__out_of_card__          = None
        public.__action_list__          = None
        public.__discard_player__       = None
        public.__discard__
        ## private info
        self.private_state          = MahjongPrivateState()
        private                          = self.private_state
        private.__keep_cards__           = self.__params__["allcards"][self.num_players*12 + 1:]
 
        ## person info
        self.person_states          = [MahjoingPersonState() for i in range(self.__params__["num_players"])]
        persion                         = self.person_states
        hand_cards       = []
        for i in xrange(self.__params__["num_players"]):
            persion[i].__id__ = i
            persion[i].__hand_cards__ = self.__params__["allcards"][i*12:(i+1)*12].sort(MahjongCard.compare)
        persion[self.__dealer_id__].__hand_cards__.append(allcards[self.num_players*12])
        persion[public.turn].__available_actions__ = self.available_actions(pu,persion[public.turn])
        self.__gen_history__()
        infos = self.__gen_infos__()
        if self.logger.level <= logging.DEBUG:
                self.logger.debug("TexasHoldemEnv.init: num_players = %d, dealer_id = %d, chip = %d, big_blind_bet = %d"%(\
                    public.num_players,\
                    public.dealer_id,\
                    public.chips[0],\
                    public.big_blind_bet
                ))

            return infos, pu, persion, pr
    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        public  = self.public_state
        persion = self.person_states
        private = self.private_state
        """[summary]
        
        动作为胡,直接game_over,计算得分
        """
        if action.effective == True and action.option == MahjongCard.Win:
            public.__previous_id__      = public.__turn__
            public.__previous_action__  = action
            public.__is_terminal__      = true
            public.__scores__             = self.__compute_scores__()
            return infos,public,persion,private
        
        """[summary]
        动作为吃,或者碰，还是这个人出牌
        """
        if action.effective == True and (action.option == MahjongCard.Pong or action.option == MahjongCard.Chow)
            public.__previous_id__      = public.__turn__
            public.__previous_action__  = action
            
            '''[summary]
            
            将碰的牌记录到public_state
            '''
            if action.option == MahjongCard.Pong:
                pong = persion[public.__turn__].__discard__
                pong.append(MahjongCard(action.__card__))
                public.__players_pong__.append((public.__discard_player__,public.__turn__,pong))
            '''[summary]
            
            将吃的牌记录到public_state
            '''
            if action.option == MahjongCard.Chow:
                chow = persion[public.__turn__].__discard__
                chow.append(MahjongCard(action.__card__))
                public.__players_chow((public.__discard_player__,public.__turn__,chow))

            persion[public.__turn__].__discard__           = []
            public.__turn__                                = public.__turn__
            persion[public.__turn__].__available_actions__ = self.available_actions(public,persion[public.__turn__])
            return infos,public,persion,private

        """[summary]
        
        动作为杠
        """
        if action.effective == True and action.option == MahjongCard.Kong:
            public.__previous_id__      = public.__turn__
            public.__previous_action__  = action
            kong                        = persion[public.__turn__].__discard__
            kong.append(MahjongCard(action.__card__))
            persion[public.__turn__].__discard__ = []
            public.__players_kong__.append((public.__discard_player__,public.__turn__,kong))
            persion[public.__turn__].__add_card__(private.__keep_cards__.pop())
            public.__turn__                                = public.__turn__
            persion[public.__turn__].__available_actions__ = self.available_actions(public,persion[public.__turn__])
            return infos,public,persion,private
        if action.effective == True and action.option == MahjongCard.ConKong:
            public.__previous_id__               = public.__turn__
            public.__previous_action__           = action
            persion[public.__turn__].__discard__ = []
            public.conkong[public.__turn__]      = public.conkong[public.__turn__] + 1
            persion[public.__turn__].__add_card__(private.__keep_cards__.pop())
            public.__turn__                                = public.__turn__
            persion[public.__turn__].__available_actions__ = self.available_actions(public,persion[public.__turn__])
            return infos,public,persion,private
        if action.effective == True and action.option == MahjongCard.Discard:
            public.__discard_player__ = public.__turn__
            public.__discard_card__   = MahjongCard(action.__card__)
        i = self.__turn__ + 1 % self.__params__["num_players"]
        while (i != self.__discard_player__):
            available_actions = self.available_actions_win(public,persion[i])
            if len(available_actions) != 0:
                public.__previous_id__     = public.__turn__
                public.__previous_action__ = action
                persion[i].__available_actions__ = available_actions
                public.__turn__ = i
                return infos,public,persion,private
        while (i != self.__discard_player__):
            available_actions = self.available_actions_special(public,persion[i])
            if len(available_actions) != 0:
                public.__previous_id__     = public.__turn__
                public.__previous_action__ = action
                persion[i].__available_actions__ = available_actions
                public.__turn__ = i
                return infos,public,persion,private
        public.__previous_id__ = public.__turn__
        public.__previous_action__ = action
        public.__turn__ = public.__discard_player__ + 1 % self.__params__["num_players"]
        available_actions = self.available_actions_chow(public,persion[public.__turn__])
        if len(available_actions) == 0:
            persion[public.__turn__].__add_card__(private.__keep_cards__.pop())
            available_actions = self.available_actions(public,persion[public.__turn__])
        persion[public.__turn__].__available_actions__ 
        return infos,public,persion,private
            
    
            
    @classmethod
    def available_actions(cls, public_state, person_state):
        '''
        Generate all valid actions given the public state and the persion state
        :param public_state:
        :parre person_state:
        :return:all valid actions
        '''
        public  = public_state
        persion = person_state
        turn    = public.turn
        key_actions = dict()
        available_actions = {}

    def available_actions_chow(cls, public_state, person_state):
        public  = public_state
        persion = person_state
        turn    = public.turn
        key_actions = dict()
        available_actions = {}
        discard = public.__discard_card__
        isExistChow = False

        for i in range(len(person_state.keep_cards) - 1):
            if MahjongCard.isSequence(discard,persion.keep_cards[i],persion.keep_cards[i + 1]) == True:
                isExistChow = True
            elif MahjongCard.isSequence(persion.keep_cards[i],discard,persion.keep_cards[i + 1]) == True:
                isExistChow = True
            elif MahjongCard.isSequence(persion.keep_cards[i],persion.keep_cards[i + 1], discard) == True:
                isExistChow = True
            if isExistChow == True:
                if available_actions[MahjongCard.Chow] is None or len(available_actions[MahjongCard.Chow]) == 0:
                    available_actions[MahjongCard.Chow] = []
                available_actions[MahjongCard.Chow].append((persion.keep_cards[i],persion.keep_cards[i + 1]))
                isExistChow = False
        return available_actions

    def available_actions_win(cls,public_state,person_state)
        public  = public_state
        persion = person_state
        turn    = public.turn
        key_actions = dict()
        available_actions = {}
        discard = public.__discard_card__
        cards = []
        isInsert = False
        for each in person_state.keep_cards:
            if MahjongCard.compare(each,discard) < 0 or isInsert == True:
                cards.append(each.__deepcopy__())
            else isInsert == False:
                cards.append(discard.__deepcopy__())
                cards.append(each.__deepcopy__())
                isInsert == True
        if MahjongCard.isWin(cards) == True:
            available_actions[MahjongCard.Win] = [discard]

    @classmethod
    def compete(cls, env, players):
        '''   
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: the winer
        '''
        num_players = len(players)
        infos, public, person, private = env.init({"num_players":num_players})
        for i in range(evn.num_players):
            players[i].receive_info(infos[i])

        while public.is_terminal == False:
            turn = public.turn
            action = players[turn].take_action()
            infos,public,persons,private = env.forward(action)
             
            for i in range(eve.__params__["num_players"]):
                players[i].receive_info(infos[i])

        return public.scores


     
