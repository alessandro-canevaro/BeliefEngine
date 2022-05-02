
from sympy import symbols 
from sympy.logic.boolalg import And, Or, Not
from BeliefBase import Belief, BeliefBase
import Resolution


def successPostulateContraction():
    bb = BeliefBase([], [])
    x, y = symbols('x, y')
    bb.expand(Belief(x))
    bb.expand(Belief(y))
    bb.contraction(Belief(x))
    assert x not in bb.formulaList

def successPostulateRevision():
    bb = BeliefBase([], [])
    x, y = symbols('x, y')
    bb.expand(Belief(~x))
    bb.expand(Belief(y))
    bb.revise(Belief(x))
    assert x in bb.formulaList

def inclusionPostulateContraction():
    bb = BeliefBase([], [])
    x, y = symbols('x, y')
    bb.expand(Belief(x))
    bb.expand(Belief(y))
    bb.contraction(Belief(x))
    assert set(bb.formulaList).issubset(set([x, y]))

def inclusionPostulateRevision():
    bb1 = BeliefBase([], [])
    bb2 = BeliefBase([], [])
    x, y = symbols('x, y')
    bb1.expand(Belief(x))
    bb1.expand(Belief(y))
    bb2.expand(Belief(x))
    bb2.revise(Belief(y))
    assert set(bb1.formulaList).issubset(set(bb2.formulaList))

def vacuityPostulateContraction():
    bb = BeliefBase([], [])
    x, y = symbols('x, y')
    bb.expand(Belief(x))
    bb.contraction(Belief(y))
    assert set(bb.formulaList) == set([x])

def vacuityPostulateRevsion():
    bb1 = BeliefBase([], [])
    bb2 = BeliefBase([], [])
    x, y = symbols('x, y')
    bb1.expand(Belief(x))
    bb1.expand(Belief(y))
    bb2.expand(Belief(x))
    bb2.revise(Belief(y))
    assert bb1 == bb2

def extensionalityPostulatecontraction():
    bb1 = BeliefBase([], [])
    bb2 = BeliefBase([], [])
    x, y = symbols('x, y')
    bb1.expand(Belief(x))
    bb1.expand(Belief(And(Or(Not(y), x), Or(Not(x), y))))
    bb1.contraction(Belief(x))
    bb2.expand(Belief(x))
    bb2.expand(Belief(And(Or(Not(y), x), Or(Not(x), y))))
    bb2.contraction(Belief(y))
    assert bb1 == bb2

def extensionalityPostulateRevision():
    bb1 = BeliefBase([], [])
    bb2 = BeliefBase([], [])
    x, y = symbols('x, y')
    bb1.expand(Belief(x))
    bb1.expand(Belief(And(Or(Not(y), x), Or(Not(x), y))))
    bb1.revise(Belief(x))
    bb2.expand(Belief(x))
    bb2.expand(Belief(And(Or(Not(y), x), Or(Not(x), y))))
    bb2.revise(Belief(y))
    for b in bb1.formulaList:
        if not Resolution.PL_Resolution(bb2.formulaList, b):
            assert False
    for b in bb2.formulaList:
        if not Resolution.PL_Resolution(bb1.formulaList, b):
            assert False
    assert True

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