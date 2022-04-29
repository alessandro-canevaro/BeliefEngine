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

def contraction(self, belief, value):
remainders = self.getRemainders(belief)
value = float(value)

maxCertaintyGlobal = 0.0
if self.values:
    maxCertaintyGlobal = max(self.values.values())

maxCertainty = -10 ** 10
maxCertaintyCombined = 0.0
bestRemainder = []
# Find the remainder containing the highest certainty value
# If there are more than one remainder containing the highest certainty value,
# choose the one with the highest combined certainty
for r in remainders:
    tmpSum = sum(self.values[str(c)] for c in r)
    for c in r:
        tmpValue = self.values[str(c)]
        if tmpValue > maxCertainty:
            maxCertainty = tmpValue
            maxCertaintyCombined = tmpSum
            bestRemainder = r
        elif tmpValue == maxCertainty:
            if tmpSum > maxCertaintyCombined:
                bestRemainder = r

if maxCertainty < maxCertaintyGlobal and value < maxCertaintyGlobal:
    # By doing the revision we would remove some belief that we are more certain of
    # than the belief that we are trying to add, so we decide not to do it
    return

self.beliefs = bestRemainder

def revision(BB, belief):
    formula = to_cnf(belief)
    negFormula = ~formula
    if PL_Resolution([], negFormula):
        print('\nInconsistent formulas cannot be added to the knowledge base')
        return
    if formula in BB.beliefs and belief.value != 0:
        # Revising with a formula already in the knowledge base is updating the certainty value for that formula
        BB.beliefs.values[str(formula)] = float(belief.value)
        return
    contraction(negFormula, belief.value)
    BB.add(self.beliefs, formula, float(belief.value))

if __name__ == '__main__':
    KB = BeliefBase()