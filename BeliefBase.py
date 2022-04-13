from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
    
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