#!/bin/python
from roomai.algorithms import CRMPlayer
from roomai.algorithms import CRMAlgorithm
from roomai.kuhn       import KuhnPokerEnv
from roomai.kuhn       import KuhnPokerRandomPlayer
from roomai.kuhn       import KuhnPokerAlwaysBetPlayer
from roomai.kuhn       import KuhnPokerAction
import random

class KuhnPokerCRMPlayer(CRMPlayer):
    def __init__(self):
        self.state                     = []
        self.regrets                   = dict()
        self.strategies                = dict()

    def update_strategies(self, state, actions, targets):
        for i in xrange(len(actions)):
            state_action = "%s_%s"%(state, actions[i].get_key())
            self.strategies[state_action] = targets[i]

    def get_strategies(self, state, actions):
        probs = [1.0 for i in xrange(len(actions))]
        for  i in xrange(len(actions)):
            state_action = "%s_%s" % (state, actions[i].get_key())
            if state_action not in self.strategies:
                probs[i] = 1.0 / len(actions)
            else:
                probs[i] = self.strategies[state_action]
        return probs

    def update_regrets(self, state, actions, targets):
        for i in xrange(len(actions)):
            state_action = "%s_%s"%(state, actions[i].get_key())
            self.regrets[state_action] = targets[i]

    def get_regrets(self, state, actions):
        regrets = [0 for i in xrange(len(actions))]
        for i in xrange(len(actions)):
            state_action = "%s_%s" % (state, actions[i].get_key())
            if state_action not in self.regrets:
                regrets[i] = 0
            else:
                regrets[i] = self.regrets[state_action]
        return regrets

    def gen_state(self,info):
        card = info.person_state.card
        history = info.public_state.action_list
        return "%d_%s" % (card, "".join(history))

    def receive_info(self, info):
        self.state             = self.gen_state(info)
        self.available_actions = info.person_state.available_actions.values()

    def take_action(self):
        probs = self.get_strategies(self.state, self.available_actions)
        sum1  = sum(probs)
        for i in xrange(len(self.available_actions)):
            probs[i] /= sum1

        r    = random.random()
        sum1 = 0
        for i in xrange(len(probs)):
            sum1 += probs[i]
            if sum1 > r:
                return self.available_actions[i]

        return self.available_actions[len(self.available_actions)-1]


    def reset(self):
        pass

if __name__ == "__main__":
    env     = KuhnPokerEnv()
    player  = KuhnPokerCRMPlayer()
    player.is_train = True
    algo    = CRMAlgorithm()
    for i in xrange(100000):
        algo.dfs(env = env, player=player, p0 = 1, p1 = 1, deep = 0)

    print player.regrets
    print player.strategies
    player.is_train = False

    player_random = KuhnPokerRandomPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in xrange(100000):
        scores = KuhnPokerEnv.compete(env,[player, player_random])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in xrange(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores


    player_alwaysbet = KuhnPokerAlwaysBetPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in xrange(100000):
        scores = KuhnPokerEnv.compete(env,[player, player_alwaysbet])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in xrange(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores

    sum_scores = [0.0, 0.0]
    num = 0
    for i in xrange(100000):
        scores = KuhnPokerEnv.compete(env, [player_random, player_alwaysbet])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num += 1
    for i in xrange(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores