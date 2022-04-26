from sympy import *
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
import itertools
from math import isclose

    
class BeliefBase:
    ''' initially belief base is empty '''
    def __init__(self):
        self.beliefBase = []

    # def add_to_belief_base(self, newBelief):
    #     self.beliefBase.append(to_cnf(newBelief))

    def expansion_belief(self, belief):
        new_order = 1
        if belief not in self.beliefBase:
            new_atoms = belief.atoms()
            for b in self.beliefs:
                if new_atoms & b.formula.atoms():
                    b.order = b.order - 0.1 * b.order
        # belief with the same elements get their order updated to be lower (temporal effect)
        # if the belief with the same elements has more operators it also gets a penalty
        belief.append(new_order)
        self.beliefBase.append(belief)


    def clear_belief_base(self):
        self.beliefBase = [] # may be it can be dict or a set?
        
    def arrangeBeliefs(self):

            result = []
            prev_order = None

            for belief in self.beliefBase:
                if prev_order is None:
                    result.append(belief)
                    prev_order = belief.order
                    continue

                if isclose(belief.order,
                           prev_order):  
                    result.append(belief)

                else:
                    yield prev_order, result
                    result = [belief]
                    prev_order = belief.order

            yield prev_order, result


    def degree(self, newBelief):

            if PL_Resolution([], newBelief):

            base = []
            for order, r in self.arrangeBeliefs():  
                base += [b.newBelief for b in r]
                if PL_Resolution(base, newBelief):
                    return order
            return 0  # otherwise return 0

    def revision(self, newBelief, order, add=True):
            formula = to_cnf(newBelief) 
            negFormula = Not(formula)
            deg = self.degree(formula)

            if 0 <= order <= 1:
                if not PL_Resolution([], negFormula):
                    # Is the new belief inconsistent
                    if PL_Resolution([], formula):
                        # Is it a tautology 
                        order = 1
                    elif order <= deg:
                        self.contraction(formula, order)
                    else:
                        self.contraction(negFormula, 0)
                        self.expansion(formula, order, False)

                    if add:
                        self.add(formula, order)
            else:
                order = False
    
    '''def revision(self, newBelief):
        formula = to_cnf(newBelief)
        negFormula = Not(formula)
        self.contraction(negFormula)
        self.expansion(newBelief)'''

    def expansion(self, belief):
        formula = to_cnf(belief)
        self.beliefBase.append(to_cnf(belief))
        
    ''' contraction'''
    def contraction(self, belief):
        newBelief = to_cnf(belief)
        for b in self.beliefBase:
            if b == newBelief:
                self.beliefBase.remove(newBelief)

    def print_belief(self):
        pass

    def show_current_belief_base(self):
        print ("Current Belief Base: ", self.beliefBase)
    
    #Not sure we need this class. Maybe is helpful only when we do the part with plausible belief
    """      
    class Belief:
        ''' it gets the formula to convert it into cnf form '''
        def __init__(self, formula) -> None:
            self.formula = formula
            self.newcnf = to_cnf(formula)
    """

#perhaps this part should go in a separate file

def PL_Resolution(KB, alpha):
    """Algorithm to check if alpha is entailed in KB.
       return true or false
    """

    # Split base into conjuncts
    clauses = split(KB+[to_cnf(~alpha)], And)

    # Special case if one clause is already False
    if False in clauses:
        return True

    new = set()
    while True:
        for Ci, Cj in itertools.combinations(clauses, 2):
            resolvents = PL_Resolve(Ci, Cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))

        if new.issubset(set(clauses)):
            return False

        #Add discovered clauses
        for c in new:
            if c not in clauses:
                clauses.append(c)

def PL_Resolve(Ci, Cj):
    """Returns the set of all possible clauses obtained by resolving its two inputs.
    """

    clauses = []
    Ci_d, Cj_d = split([Ci], Or), split([Cj], Or)

    for i in Ci_d:
        for j in Cj_d:
            # If di, dj are complementary
            if i == ~j or ~i == j:
                # Create list of all disjuncts except di and dj
                res = [k for k in Ci_d if k != i] + [k for k in Cj_d if k != j]
                # Remove duplicates
                res = list(set(res))
                # Join into new clause
                res = split(res, Or)
                if len(res) == 0:
                    clauses.append(Or.identity)
                elif len(res) == 1:
                    clauses.append(res[0])
                else:
                    clauses.append(Or(*res))

    return clauses

def split(clause, op):
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(clause)
    return result


if __name__ == "__main__":
    x, y = symbols('x,y')
    print(PL_Resolve(x | (y | x >> y), Not(x >> y)))
    print(PL_Resolve(x | y, Not(x) | Not(y)))
    #print(False in x)
    print(PL_Resolution([x|y], x))
    print(PL_Resolution([x], x|y))

formula= [x|y,1]
beliefbase=[[x|y,1],[x,0.2]]