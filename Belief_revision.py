import itertools

from numpy.core.numerictypes import maximum_sctype
from sympy.logic.boolalg import to_cnf, Or, And
from BeliefBase import BeliefBase
from Resolution import *
import numpy as np

def Partial_meet_contraction(BB, formula):
    old_KB = KB.beliefBase

''' contraction'''
def Belief_Contraction(KB, belief):
    newBelief = to_cnf(belief)
    for b in KB.beliefBase:
        if b == newBelief:
            KB.beliefBase.remove(newBelief)

def contract(BB, belief):
    if PL_Resolution([], belief.formula):
        # it is tautology -> should be ignored
        return

    oldrank = self.rank(formula)
    delta = BeliefBase()
    delta.beliefs = self.beliefs.copy()
    for belief in self.beliefs:
        if belief.rank <= oldrank:
            bb = [to_cnf(x.formula) for x in filter(lambda x: x.rank >= (oldrank + 1), delta.beliefs)]
            bb = reduce(lambda x, y: x & y, bb, true)
            if not entails(bb, formula | belief.formula):
                r = delta.rank(belief.formula)
                delta.beliefs.remove(belief)
                print(f">>> {belief} removed by (C-) condition")
                if r < oldrank or not entails(bb, formula >> belief.formula):
                    for b in self.beliefs:
                        if formula >> belief.formula == b.formula:
                            delta.beliefs.remove(b)
                    t = Belief(formula >> belief.formula, r)
                    delta.beliefs.add(t)
                    print(f">>> Added {t} to belief basis to satisfy (K-5)")
    self.beliefs = delta.beliefs

def revision(BB, formula, newrank):
    if 0 <= newrank:
        contract(Not(formula))
        BB.expand(formula, newrank)
    else:
        print(f"Rank {newrank} is negative.\nRevision not done.")

if __name__ == '__main__':
    KB = BeliefBase()