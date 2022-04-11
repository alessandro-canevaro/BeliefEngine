from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
    
class BeliefBase:
    ''' initially belief base is empty '''
    def __init__(self):
        self.beliefBase = []

    def add_to_belief_base(self, value):
        pass

    def clear_belief_base(self):
        ''' may be it can be dict'''
        self.beliefBase = {} 
    
    def revision(self, formula):
        pass

    def expansion(self, belief: Belief):
        pass

    def contraction(self, belief: Belief):
        pass

    def print_belief(self):
        pass

    def show_current_belief_base(self):
        print ("Current Belief Base: " + self.beliefBase)
    
        


class Belief:
    ''' it gets the formula to convert it into cnf form '''
    def __init__(self, formula) -> None:
        self.formula = formula
        self.newcnf = to_cnf(formula)