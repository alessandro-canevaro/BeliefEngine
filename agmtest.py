
from sympy import  Implies, symbols 
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
from BeliefBase import Belief, BeliefBase
import Resolution


def successPostulateContraction():
    alpha = symbols('x')
    bb = BeliefBase()
    if Resolution.PL_Resolution({}, alpha):
        assert False
    bb.contraction(Belief(alpha))
    assert not Resolution.PL_Resolution(bb.getclauses(), alpha)

def successPostulateRevision():
    bb = BeliefBase()
    alpha = symbols('x')
    bb2 = bb.revision(Belief(alpha))
    assert bb2.beliefs.issubset(bb)

def inclusionPostulateContraction():
    bb = BeliefBase()
    alpha = symbols('x')
    bb.contraction(Belief(alpha))
    assert Resolution.PL_Resolution(bb.getclauses(), alpha)

def inclusionPostulateRevision():
    bb1 = BeliefBase()
    bb2 = BeliefBase()
    alpha = symbols('x')
    bb1.revision(Belief(alpha))
    bb2.expand(Belief(alpha))
    assert bb1.beliefs.issubset(bb2.beliefs)


def vacuityPostulateContraction():
    bb = BeliefBase()
    alpha = symbols('x')
    if Resolution.PL_Resolution(bb.getclauses(), alpha):
        assert False
    bb2 = bb.contract(Belief(alpha))
    assert bb == bb2

def vacuityPostulateRevsion():
    bb = BeliefBase()
    alpha = symbols('x')
    bb2 = BeliefBase()

    if Resolution.PL_Resolution(bb.getclauses(), ~alpha):
        assert False

    bb.revision(Belief(alpha))
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

