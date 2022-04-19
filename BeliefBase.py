from sympy import *
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
    
class BeliefBase:
    ''' initially belief base is empty '''
    def __init__(self):
        self.beliefBase = []

    def add_to_belief_base(self, newBelief):
        self.beliefBase.append(to_cnf(newBelief))

    def clear_belief_base(self):
        self.beliefBase = [] # may be it can be dict or a set?
    
    def revision(self, newBelief):
        formula = to_cnf(newBelief)
        negFormula = ~formula
        #do stuff...

    def expansion(self, belief):
        pass

    def contraction(self, belief):
        pass

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
    pass

def PL_Resolve(Ci, Cj):
    """Returns the set of all possible clauses obtained by resolving its two inputs.
    """

    clauses = []
    Ci_d, Cj_d = disjuncts([Ci]), disjuncts([Cj])

    for i in Ci_d:
        for j in Cj_d:
            # If di, dj are complementary
            if i == ~j or ~i == j:
                # Create list of all disjuncts except di and dj
                res = [k for k in Ci_d if k != i] + [k for k in Cj_d if k != j]
                # Remove duplicates
                res = list(set(res))
                # Join into new clause
                res = disjuncts(res)
                if len(res) == 0:
                    clauses.append(Or.identity)
                elif len(res) == 1:
                    clauses.append(res[0])
                else:
                    clauses.append(Or(*res))

    return clauses

def disjuncts(clause):
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, Or):
                collect(arg.args)
            else:
                result.append(arg)

    collect(clause)
    return result


if __name__ == "__main__":
    x, y = symbols('x,y')
    print(PL_Resolve(x | (y | x >> y), Not(x >> y)))
    print(PL_Resolve(x | y, Not(x) | Not(y)))