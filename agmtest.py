
from sympy import  Implies, symbols 
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
from BeliefBase import Belief, BeliefBase
import Resolution


def successPostulateContraction():
    alpha = symbols('x')
    bb = BeliefBase()
    if Resolution.PL_Resolution([], alpha):
        assert False
    bb.contract(Belief(alpha))
    assert not Resolution.PL_Resolution(bb.getclauses(), alpha)

def successPostulateRevision():
    bb = BeliefBase()
    alpha = symbols('x')
    bb.revise(Belief(alpha))
    assert alpha in bb.formulaList

def inclusionPostulateContraction():
    bb = BeliefBase()
    x, y = symbols('x, y')
    bb.expand(Belief(x))
    bb.expand(Belief(y))
    bb.contract(Belief(x))
    assert y in bb.formulaList

def inclusionPostulateRevision():
    bb1 = BeliefBase()
    bb2 = BeliefBase()
    x, y = symbols('x, y')
    bb1.expand(Belief(x))
    bb1.expand(Belief(y))
    bb2.expand(Belief(x))
    bb2.revise(Belief(y))
    assert set(bb1.formulaList) == set(bb2.formulaList)

def vacuityPostulateContraction():
    bb = BeliefBase()
    x, y = symbols('x, y')
    bb.expand(Belief(x))
    bb.contract(Belief(y))
    assert x in bb.formulaList

def vacuityPostulateRevsion():
    bb = BeliefBase()
    alpha = symbols('x')
    bb2 = BeliefBase()

    if Resolution.PL_Resolution(bb.getclauses(), ~alpha):
        assert False

    bb.revise(Belief(alpha))
    bb2.expand(Belief(alpha))
    assert bb == bb2

def extensionalityPostulatecontraction():
    x , y = symbols('x,y')
    bb1 = BeliefBase()
    bb2 = BeliefBase()
    '''phi = Implies(x , y)'''
    phi = Or(Not(y), x)
    xi = Or(Not(x), y)
    alpha = And(phi, xi)

    if Resolution.PL_Resolution({}, alpha):
        assert False

    bb1.contract(Belief(phi))
    bb2.contract(Belief(xi))
    assert bb1 == bb2

def extensionalityPostulateRevision():
    x , y = symbols('x,y')
    bb1 = BeliefBase()
    bb2 = BeliefBase()
    phi = Or(Not(y), x)
    xi = Or(Not(x), y)
    alpha = And(phi, xi)

    if Resolution.PL_Resolution({}, alpha):
        assert False

    bb1.revision(Belief(phi))
    bb2.revision(Belief(xi))

    assert bb1 == bb2

def consistencyPostulate():
    pass



if __name__ == "__main__":
    successPostulateContraction()
    successPostulateRevision()
    inclusionPostulateContraction()
    inclusionPostulateRevision()
    vacuityPostulateContraction()
    vacuityPostulateRevsion()
    extensionalityPostulatecontraction()
    extensionalityPostulateRevision()
    consistencyPostulate()
    print("all test passed")