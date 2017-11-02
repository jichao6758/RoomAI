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
        ## private info
        self.private_state          = MahjongPrivateState()
        pr                          = self.private_state
        pr.__keep_cards__           = self.__params__["allcards"][self.num_players*12 + 1:]

        ## person info
        self.person_states          = [MahjoingPersonState() for i in range(self.__params__["num_players"])]
        pes                         = self.person_states
        hand_cards       = []
        for i in range(self.__params__["num_players"]):
            pes[i].__id__ = i
            pes[i].__hand_cards__ = self.__params__["allcards"][i*12:(i+1)*12]
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

        if not self.is_action_valid(action, pu, pe[pu.turn]):
            self.logger.critical("action=%s is invalid" % (action.key))
            raise ValueError("action=%s is invalid" % (action.key))
        for i in range(self.__params__["num_players"]):

            available_actions = self.available_actions(pu,pes[pu.turn])
            for each_action in available_actions:
                if each_action == MahjongAction.Kong:
                    break
            
    @classmethod
    def compete(cls, env, players):
        '''   
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: the winer
        '''
        action = [0 for i in range(len(players))]
        while len(keep_cards) != 0:


     
