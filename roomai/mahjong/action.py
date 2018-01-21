#!/bin/python
from MahjongEnv import MahjongEnv
from MahjongAction import MahjongAction
from MahjongEnv import MahjongEnv
from MahjongInfo import *
from MahjongUtil import *
import sys
sys.path.append("d:/RoomAI/")
sys.path.append("/Users/jichao/Desktop/RoomAI")
import roomai.common
from roomai.common import AbstractPlayer
class RandomPlayer(AbstractPlayer):
    '''
    The RandomPlayer is a player, who randomly takes an action.
    The RandomPlayer is as a common baseline
    '''
    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    def take_action(self):
        import random
        idx = int(random.random() * len(self.available_actions))
        action = list(self.available_actions.values())[idx]
        action.effective = True
        return action

    def reset(self):
        pass

if __name__ == '__main__':
    players = [RandomPlayer() for i in range(4)]
    env = MahjongEnv()
    #print env.__params__

    scores = MahjongEnv.compete(env, players)
    # print scores