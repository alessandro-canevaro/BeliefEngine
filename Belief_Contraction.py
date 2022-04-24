import itertools

from numpy.core.numerictypes import maximum_sctype
from sympy.logic.boolalg import to_cnf, Or, And
from BeliefBase import BeliefBase, PL_Resolution, PL_Resolve, split
import numpy as np

def Belief_Contraction(KB, formula):
    old_KB = KB.beliefBase

if __name__ == '__main__':
    KB = BeliefBase()