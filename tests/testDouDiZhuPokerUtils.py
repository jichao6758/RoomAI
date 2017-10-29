#!/bin/python

import sys
import unittest
from roomai.doudizhu import *

class DouDiZhuPokerUtilTester(unittest.TestCase):
    """
    """
    def testAction2Patterns(self):
        """

        """
        
        a = DouDiZhuPokerAction([1, 1, 1], [2])
        self.assertEqual(a.pattern[0], "p_3_1_0_1_0")

        a = DouDiZhuPokerAction([1, 1, 1, 2, 3, 3], [])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = DouDiZhuPokerAction([1, 1, 1, 1, 1], [2])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [2])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        self.assertEqual(a.pattern[0], "i_cheat")
        
        a = DouDiZhuPokerAction([DouDiZhuActionElement.R, DouDiZhuActionElement.r], [])
        self.assertEqual(a.pattern[0], "x_rocket")
        

    def testAllPatterns(self):
        """

        """
        for k in AllPatterns:
            p = AllPatterns[k]
            self.assertEqual(k,p[0])
            self.assertEqual(len(p),7)
            if "p" in p[0]:
                self.assertEqual("p_%d_%d_%d_%d_%d"%(p[1],p[2],p[3],p[4],p[5]), p[0])

    def testActions(self):
        """

        """
        from roomai.doudizhu.DouDiZhuPokerAction import  DouDiZhuPokerAction as Action
        a = Action.lookup("3333")

        print a.pattern
        assert(a.pattern[0] == "p_4_1_0_0_0")
