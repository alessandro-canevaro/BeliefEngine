from sympy import *
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
import itertools

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
    print("end\n")
    #print(False in x)
    print(PL_Resolution([x|y], x))
    print(PL_Resolution([x], x|y))
    print("---------------------")
