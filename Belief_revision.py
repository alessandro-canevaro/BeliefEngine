import itertools

from numpy.core.numerictypes import maximum_sctype
from sympy.logic.boolalg import to_cnf, Or, And, Equivalent, Not
from BeliefBase import BeliefBase, _check_value, Belief
from Resolution import *
import numpy as np


''' contraction'''
def SimpContraction(KB, belief):
    newBelief = to_cnf(belief)
    for b in KB.beliefBase:
        if b == newBelief:
            KB.beliefBase.remove(newBelief)

def general_Remainders(BB, belief):
    new_belief = to_cnf(belief)
    remainders = []
    if not PL_Resolution(BB.formulaList, new_belief):
        # Whole knowledge base is solution
        remainders.append(BB.formulaList)
        return remainders

    beliefsList = BB

    def contract(BeliefsList, beliefToRemove):
        if len(BeliefsList) == 1:
            if not PL_Resolution(BeliefsList, beliefToRemove):
                remainders.append(BeliefsList)
            return

        for i in BeliefsList:

            tmpBeliefs = [belief for belief in BeliefsList if belief != i]

            if tmpBeliefs is not None:
                if PL_Resolution(tmpBeliefs, beliefToRemove):
                    # Implies beliefToRemove, have to remove more
                    contract(tmpBeliefs, beliefToRemove)
                else:
                    # Does not imply beliefToRemove, one of the possible remainders
                    remainders.append(tmpBeliefs)

    contract(beliefsList.formulaList, new_belief)

    print("raw_remainders:")
    print(remainders)
    # delete duplicates belief
    resRemainders = []
    for i in remainders:
        flag = 0
        for j in resRemainders:
            if i == j:
                flag = 1
        if flag == 0:
            resRemainders.append(i)
    print('resRemainders:')
    print(resRemainders)

    return resRemainders

def contraction(BB, belief, value=None):
    remainders = general_Remainders(BB, belief)
    new_BB = BeliefBase()

    bestRemainder = []
    remainderlens = []
    for r in remainders:
        remainderlens.append(len(r))
    bestRemainder = remainders[remainderlens.index(max(remainderlens))]

    for b in bestRemainder:
        for ob in BB.beliefs:
            if ob.formula == b:
                new_BB.expand(ob)

    # new_BB.print_belief()
    return new_BB


def revision(BB, formula, value=None):
    belief = Belief(formula, value)
    formula = belief.formula
    negFormula = ~formula
    if PL_Resolution([], negFormula):
        print('\nInconsistent formulas cannot be added to the knowledge base')
        return
    if value is not None:
        if not _check_value(value):
            return
    new_BB = contraction(BB, negFormula)
    new_BB.expand(belief)
    new_BB.print_belief()
    return new_BB

if __name__ == '__main__':
    x, y, z= symbols('x,y,z')
    bb = BeliefBase()
    bb.expand(Belief(x))
    bb.expand(Belief(x & y))
    bb.expand(Belief(x | y & z))
    bb.expand(Belief(y & z))
    # bb.expand(Belief(~z))
    bb.print_belief()
    # bb.expand(Belief(x | z)) #contraddiction is not added
    # bb = contraction(bb, ~z)
    bb.print_belief()
    bb = revision(bb, ~z)


