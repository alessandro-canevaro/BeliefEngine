from sympy import *
from sympy.logic.boolalg import to_cnf
from Resolution import PL_Resolution


def _check_value(value):
    '''
    Description:
        Checks the value of the belief is withing range (0=<n<=1)
    '''
    flag = True
    if not ((0 < value) and (value <= 1)):
        print("the value of belief should be in the range(0,1]")
        flag = False
    return flag


class Belief:
    def __init__(self, formula, value=None) -> None:
        self.formula = to_cnf(formula)
        self.value = value

class BeliefBase:
    ''' initially belief base is empty '''
    def __init__(self, beliefs=[], formulaList=[]):
        self.beliefs = beliefs  # list of Belief objects
        self.formulaList = formulaList  # List of Beliefs formula, use to PL_resolution
        self.decrease_constant = 0.1

    def __eq__(self, BB):
        return set(self.formulaList) == set(BB.formulaList)

    def _removeBelief(self, formula):
        for i, b in enumerate(self.beliefs):
            if b.formula == formula:
                self.beliefs.pop(i)
                self.formulaList.pop(i)

    def expand(self, belief: Belief):
        if PL_Resolution([], ~belief.formula):
            print("the belief is a contraddiction!")
            # it is contraddiction -> should be ignored
            return

        if belief.value is None:
            symbols_set = belief.formula.free_symbols
            for b in self.beliefs:
                if symbols_set.intersection(b.formula.free_symbols):
                    b.value -= b.value * self.decrease_constant
            belief.value = 1
        elif not _check_value(belief.value):
            return

        self._removeBelief(belief.formula)
        self.beliefs.append(belief)
        self.formulaList.append(belief.formula)

    ''' contraction'''
    def SimpContraction(self, KB, belief):
        newBelief = to_cnf(belief)
        for b in KB.beliefBase:
            if b == newBelief:
                KB.beliefBase.remove(newBelief)

    def generate_Remainders(self,belief):
        new_belief = to_cnf(belief)
        remainders = []
        if not PL_Resolution(self.formulaList, new_belief):
            # Whole knowledge base is solution
            remainders.append(self.formulaList)
            return remainders

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

        contract(self.formulaList, new_belief)

        #print("raw_remainders:")
        #print(remainders)
        # delete duplicates belief
        resRemainders = []
        for i in remainders:
            flag = 0
            for j in resRemainders:
                if i == j:
                    flag = 1
            if flag == 0:
                resRemainders.append(i)
        #print('resRemainders:')
        #print(resRemainders)

        return resRemainders

    def contraction(self, belief):
        remainders = self.generate_Remainders(belief.formula)
        old_beliefs = self.beliefs
        self.clear_belief_base()

        def valueSum(Beliefs, remainders):
            sum_value = 0
            for rb in remainders:
                for be in Beliefs:
                    if be.formula == rb:
                        sum_value = sum_value + be.value

            return sum_value
        if len(remainders) > 0:
            bestRemainders = []
            remainderlens = []
            remaindersvalues = []
            for r in remainders:
                remainderlens.append(len(r))
            print(max(remainderlens))
            for i in remainderlens:
                if i == max(remainderlens):
                    bestRemainders.append(remainders[remainderlens.index(i)])
                    sum = float(valueSum(old_beliefs, remainders[remainderlens.index(i)]))
                    remaindersvalues.append(sum)

            bestRemainder = bestRemainders[remaindersvalues.index(max(remaindersvalues))]

            for b in bestRemainder:
                for ob in old_beliefs:
                    if ob.formula == b:
                        self.expand(ob)

    def revise(self, belief):
        formula = belief.formula
        negFormula = ~formula
        if PL_Resolution([], negFormula):
            print('\nInconsistent formulas cannot be added to the knowledge base')
            return
        if belief.value is not None:
            if not _check_value(belief.value):
                return
        self.contraction(Belief(negFormula))
        self.expand(belief)
        #self.print_belief()

    def clear_belief_base(self):
        self.beliefs = [] 
        self.formulaList = []

    def getclauses(self):
        return [belief.formula for belief in self.beliefs]

    def print_belief(self):
        if self.beliefs:
            for b in self.beliefs:
                print(b.formula, b.value)
            #print(self.formulaList)

        else:
            print("The belief base is empty")


if __name__ == "__main__":
    x, y, z = symbols('x,y,z')

    bb = BeliefBase()
    bb.expand(Belief(x))
    bb.expand(Belief(x & y))
    bb.expand(Belief(x | y))  # contraddiction is not added
    bb.expand(Belief(x >> y))  # only the duplicate with the highest order is kept
    bb.expand(Belief(y >> x))
    # print(type(bb.beliefs[0].formula))
    print(PL_Resolution(bb.formulaList, y))
    # bb.expand(Belief(y, 0.3))  # add belief with specific value
    bb.print_belief()
    bb.contraction(Belief(x))

    bb.print_belief()
    bb._removeBelief(x & y)
    bb.print_belief()
    bb.expand(Belief(y & z))
    bb.print_belief()
