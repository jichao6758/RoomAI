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
        public.__discard_player__       = -1
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
            public.__scores__             = self.__compute_scores__(self.public_state)
            return infos,public
        
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
            persion[public.__turn__].__available_actions__ = sefl.available_actions
            return infos,public,persion,private
        if action.effective == True and action.option == MahjongCard.ConKong:
            public.__previous_id__               = public.__turn__
            public.__previous_action__           = action
            persion[public.__turn__].__discard__ = []
            public.conkong[public.__turn__]      = public.conkong[public.__turn__] + 1
            persion[public.__turn__].__add_card__(private.__keep_cards__.pop())
            public.__turn__                      = public.__turn__
        if action.effective == True and action.option == MahjongCard.Discard:
            public.__discard_player__ = public.__turn__
        i = public.__turn__
        
            #for player_num in xrange(self.__params__["num_players"]):
            #     if self.__action_list__[player_num].isExistKong == True:
            #       public.__previous_id__                                       = public.turn
            #       public.__previous_action__                                   = action
            #       public.__is_terminal__                                       = False
            #       public.__turn__                                              = i
            #       pe[self.public_statue.previous_id].__available_actions__ = {}
            #       pe[self.public_statue.turn].__available_actions__        = self.effective
        #if action.effective == False:
            # i = public.__turn__ + 1
            # while (i % self.__params__["num_players"] != public.__previous_id__):
            #     available_action = self.__is_kong__(self,i)
            #     if available_action is not None:
            #         public.__previous_id__     = public.__turn__
            #         public.__previous_action__ = action
            #         public.__turn__ = i 

            #         pe[self.public_state.previous_id].__available_actions__ = dict()
            #         pe[self.public_state.turn].__available_actions__ = self.available_actions()
            #         self.__gen_history__()
            #         infos = self.__gen_infos__()
            #         return infos, public_state, person_states, private_state
            
        if not self.is_action_valid(action, pu, pe[public.turn]):
            self.logger.critical("action=%s is invalid" % (action.key))
            raise ValueError("action=%s is invalid" % (action.key))
            
        if action.option == MahjongCard.Win:
            self.__action_win__(action)
            public.__is_terminal__ = 
    def __action_win__(self,action):
        '''check win compute score
        
        [description]
        
        Arguments:
            action {[type]} -- [description]
        '''

        
    @classmethod
    def available_actions(cls, public_state, person_state):
        '''
        Generate all valid actions given the public state and the persion state
        :param public_state:
        :parre persion_state:
        :return:all valid actions
        '''
        pu = public_state
        pe = persion_state
        turn = public.turn
        key_actions = dict()
        available_actions = {}
        for i in xrange(self.__params__["num_players"]):
            available_actions
    @classmethod
    def compete(cls, env, players):
        '''   
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: the winer
        '''
        while public.is_terminal == False:
            turn = public.turn
            action = players[turn].take_action()
            infos,public,persons,private = env.forward(action)
        



     
