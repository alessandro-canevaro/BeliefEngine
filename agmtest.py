
from sympy import symbols
from BeliefBase import Belief, BeliefBase
import Resolution


def successPostulateContraction():
    alpha = symbols('x')
    bb = BeliefBase()
    if Resolution.PL_Resolution({}, alpha):
        assert False
    bb.contraction(Belief(alpha))
    assert not Resolution.PL_Resolution(bb.getclauses(), alpha)

def successPostulateRevision(self):
    bb = BeliefBase()
    alpha = symbols('x')
    bb2 = bb.revision(Belief(alpha))
    assert bb2.beliefs.issubset(bb)

def inclusionPostulateContraction(self):
    bb = BeliefBase()
    alpha = symbols('x')
    bb.contraction(Belief(alpha))
    assert Resolution.PL_Resolution(bb.getclauses(), alpha)

def inclusionPostulateRevision(self):
    bb1 = BeliefBase()
    bb2 = BeliefBase()
    alpha = symbols('x')
    bb1.revision(Belief(alpha))
    bb2.expand(Belief(alpha))
    assert bb1.beliefs.issubset(bb2.beliefs)


def vacuityPostulateContraction(self):
    bb = BeliefBase()
    alpha = symbols('x')
    if Resolution.PL_Resolution(bb.getclauses(), alpha):
        assert False
    bb2 = bb.contract(Belief(alpha))
    assert bb == bb2

def vacuityPostulateRevsion(self):
    bb = BeliefBase()
    alpha = symbols('x')
    bb2 = BeliefBase()

    if Resolution.PL_Resolution(bb.getclauses(), ~alpha):
        assert False

    bb.revision(Belief(alpha))
    bb2.expand(Belief(alpha))
    assert bb == bb2
