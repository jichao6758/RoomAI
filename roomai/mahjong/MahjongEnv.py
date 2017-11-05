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
        pu                          = self.public_state
        pu.__num_players            = self.public_state.__num_players
        pu.__dealer_id__            = self.public_state.__dealer_id__
        pu.__turn__                 = random.randomint(0,3)
        pu.__previous_id__          = None
        pu.__previous_action__      = None
        pu.__remaining_card_num__   = len(self.__params__["allcards"])
        pu.__out_of_card__          = None
        pu.__action_list__          = None
        ## private info
        self.private_state          = MahjongPrivateState()
        pr                          = self.private_state
        pr.__keep_cards__           = self.__params__["allcards"][self.num_players*12 + 1:]
 
        ## person info
        self.person_states          = [MahjoingPersonState() for i in range(self.__params__["num_players"])]
        pes                         = self.person_states
        hand_cards       = []
        for i in xrange(self.__params__["num_players"]):
            pes[i].__id__ = i
            pes[i].__hand_cards__ = self.__params__["allcards"][i*12:(i+1)*12].sort(MahjongCard.compare)
        pes[self.__dealer_id__].__hand_cards__.append(allcards[self.num_players*12])
        pes[pu.turn].__available_actions__ = self.available_actions(pu,pes[pu.turn])
        self.__gen_history__()
        infos = self.__gen_infos__()
        if self.logger.level <= logging.DEBUG:
                self.logger.debug("TexasHoldemEnv.init: num_players = %d, dealer_id = %d, chip = %d, big_blind_bet = %d"%(\
                    pu.num_players,\
                    pu.dealer_id,\
                    pu.chips[0],\
                    pu.big_blind_bet
                ))

            return infos, pu, pes, pr
    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        pu = self.public_state
        pe = self.person_states
        pr = self.private_state
        if action.effective == True and action.option == MahjongCard.Discard:
            actions = self.available_actions(pu,pe)
            # for player_num in xrange(self.__params__["num_players"]):
            #     if self.__action_list__[player_num].isExistKong == True:
                   pu.__previous_id__                                       = pu.turn
                   pu.__previous_action__                                   = action
                   pu.__is_terminal__                                       = False
                   pu.__turn__                                              = i
                   pe[self.public_statue.previous_id].__available_actions__ = {}
                   pe[self.public_statue.turn].__available_actions__        = self.
        if action.effective == False:

            self.__gen_history__()
            infos = self.__gen_infos__()
            return infos, public_state, person_states, private_state
        if not self.is_action_valid(action, pu, pe[pu.turn]):
            self.logger.critical("action=%s is invalid" % (action.key))
            raise ValueError("action=%s is invalid" % (action.key))
        if action.option == MahjongCard.Win:
            self.__action_win__(action)    
    def __action_win__(self,action):
        pu = self.public_state
        pe = self.person_states
        hand_cards = [c.__deepcopy__() for c in pe[pu.turn].__hand_cards__]
        if public_state.__out_of_card__ is not None:
            hand_cards.append(pu.__out_of_card__)
        if (MahjongCard.iswin(hand_cards) == True):
            pu.is_terminal = True
    
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
        turn = pu.turn
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
        



     
