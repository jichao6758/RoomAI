#!/bin/python
#coding=utf8
import roomai.common
import roomai.sevenking
#from roomai.mahjong #import AllSevenKingPatterns

#from functools import cmp_to_key

class MahjongAction(roomai.common.AbstractAction):
    # basic_action
    # 和牌
    Win             = 'Win'
    # 碰
    Pong            = 'Pong'
    # 杠
    Kong            =  'Kong'
    # 吃
    Chow            = 'Chow'
    # 暗杠(Concealed Kong)
    ConKong         = 'ConKong'
    # 打牌
    Discard         = 'Discard'
    # 不操作
    Null            = 'Null'

    
    def __init__(self, key):
        opt_list   = key.strip().split("_")
        self.__option__  = opt_list[0]
        '''
        source:-1 表示来源于环境 0 表示来源于自己手牌 其他表示来源于其他玩家对应的id

        '''
        self.__source__     = opt_list[1]
        self.__card__       = "_".join(opt_list[2:])
        self.__key__        = "%s_%s_%s"%(self.__option__, self.__source__,self.__card__)
        self.effective      = False   
    @property
    def key(self):
        return self.__key__
    @property
    def option(self):
        return self.__option__
    @property
    def source(self):
        return self.__source__
    @property
    def card(self):
        return self.__card__
    def __deepcopy__(self, memodict={}, newinstance = None):
        """

        Args:
            memodict:
            newinstance:

        Returns:

        """
        if self.key not in AllMahjongActions:
            AllMahjongActions[self.key] = MahjongAction(self.key)
        return AllMahjongActions[self.key]
    @classmethod
    def lookup(cls,key):
        if key not in AllMahjongActions:
            AllMahjongActions[key] = MahjongAction(key)
        return AllMahjongActions[key]

AllMahjongActions = dict()



