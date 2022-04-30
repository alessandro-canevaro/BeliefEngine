import itertools

from numpy.core.numerictypes import maximum_sctype
from sympy.logic.boolalg import to_cnf, Or, And, Equivalent, Not
from BeliefBase import BeliefBase,_check_value
from Resolution import *
import numpy as np


''' contraction'''
def SimpContraction(KB, belief):
    newBelief = to_cnf(belief)
    for b in KB.beliefBase:
        if b == newBelief:
            KB.beliefBase.remove(newBelief)

def general_Remainders(BB, belief):
    remainders = []
    new_belief = belief.formula.copy()
    if belief.value is not None:
        if not PL_Resolution(BB.formulaList, new_belief):
            # Whole knowledge base is solution
            return BB
    remainders = []
    allBeliefs = self.beliefs

    def contract(beliefList, beliefToRemove):
        if len(beliefList) == 1:
            if not self.resolution(beliefList, beliefToRemove):
                remainders.append(beliefList)
            return

        for i in beliefList:
            tmp = helpFunctions.removeFromList(i, beliefList)
            if self.resolution(tmp, beliefToRemove):
                # Implies beliefToRemove, have to remove more
                contract(tmp, beliefToRemove)
            else:
                # Does not imply beliefToRemove, one of the possible remainders
                remainders.append(tmp)

    contract(allBeliefs, beliefCnf)

    # Remove duplicates and remainders that are not maximal (remainders)
    remainders = helpFunctions.removeSublist(remainders)

    return remainders

def contraction(BB, belief):
    remainders = general_Remainders(BB, belief)
    new_BB = BeliefBase()
    bestRemainder = []

    for b in bestRemainder:
        for ob in BB:
            if ob.beliefs.formula == b.formula:
                new_BB.expand(b)

def revision(BB, belief):
    formula = to_cnf(belief)
    negFormula = ~formula
    if PL_Resolution([], negFormula):
        print('\nInconsistent formulas cannot be added to the knowledge base')
        return
    if belief.value is not None:
        if not _check_value(belief.value):
            return
    contraction(BB, negFormula)
    BB.expand(belief)

if __name__ == '__main__':
    KB = BeliefBase()
