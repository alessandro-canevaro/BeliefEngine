from tkinter import EW
from sympy import *
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
import itertools

    
class BeliefBase:
    ''' initially belief base is empty '''
    def __init__(self):
        self.beliefBase = []
    '''
    def add_to_belief_base(self, newBelief):
        self.beliefBase.append(to_cnf(newBelief))
    '''

    def clear_belief_base(self):
        self.beliefBase = [] # may be it can be dict or a set?
    
    def revision(self, newBelief):
        formula = to_cnf(newBelief)
        negFormula = ~formula
        self.contraction(negFormula)
        self.expansion(newBelief)
        

    def expansion(self, belief):
        formula = to_cnf(belief)
        self.beliefBase.append(to_cnf(belief))
        
    ''' contraction'''
    def contraction(self, belief):
        newBelief = to_cnf(belief)
        for b in self.beliefBase:
            if b == newBelief:
                self.beliefBase.remove(newBelief)



    def contract(self,newbelief):
        if not self.belief_base:
            return
        con_new_belief = new_belief
        new_belief_base = None
        queue = [self.belief_base]
        current_belief_base = ['I AM FILLED']

        while 



        cur_belief_base = self.belief_base

        while new_belief_base is None and current_belief_base:
            current_belief_base = queue.pop(0)
            for b in current_belief_base:
                if self.resolution(con_new_belief,current_belief_base):
                    aux_belief_base = copy(current_belief_base)
                    aux_belief_base = [bb for bb in aux_belief_base if bb.cnf_formula != b.cnf_formula]
                    queue.append(aux_belief_base)
                else:
                    new_belief_base = current_belief_base
                    break
        if new_belief_base is not None:
            self.belief_base = new_belief_base
        else:
            self.clear(False)
            return










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