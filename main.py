from BeliefBase import *
from Resolution import PL_Resolution
from sympy import *


class UserInterface:
    def __init__(self) -> None:
        self.bb = BeliefBase()
        self.action_dict = {'p': self.bb.print_belief,
                            'a': self.addBelief,
                            'r': self.reviseBelief,
                            'c': self.contractBelief,
                            'e': self.entailBelief,
                            'w': self.bb.clear_belief_base,
                            'q': quit}

    def printInstructions(self):
        print("---List of Actions---")
        print("p: Print current belief base")
        print("a: Add a new belief")
        print("r: Revise the current belief base with a new belief")
        print("c: Contract the current belief base")
        print("e: Check if a formula is entailed in the belief base")
        print("w: Clear current belief base")
        print("q: Terminate execution")
        print("---               ---")

    def selectAction(self):
        while True:
            a = input("Choose an action:")[0].lower()
            if a in "parcewq":
                return a

    def run(self):
        while True:
            print()
            self.printInstructions()
            action = self.selectAction()
            self.action_dict[action]()
            print("-----------------------------------")

    def addBelief(self):
        while True:
            try:
                formula = input("Insert the formula: ")
                print(formula)
                neg_formula = '~(' + formula + ')'
                negformula = Belief(neg_formula).formula
                if PL_Resolution(self.bb.formulaList, negformula):
                    print("Can not add the belief, need to revise")
                    self.bb.revise(Belief(formula))
                else:
                    self.bb.expand(Belief(formula))
                # self.bb.expand(Belief(formula))
                print("the new belief base is:")
                self.bb.print_belief()
                break
            except SympifyError:
                print("The formula is not valid")

    def reviseBelief(self):
        while True:
            try:
                formula = input("Insert the formula: ")
                self.bb.revise(Belief(formula))
                print("the new belief base is:")
                self.bb.print_belief()
                break
            except SympifyError:
                print("The formula is not valid")

    def contractBelief(self):
        while True:
            try:
                formula = input("Insert the formula: ")
                self.bb.contraction(Belief(formula))
                print("the new belief base is:")
                self.bb.print_belief()
                break
            except SympifyError:
                print("The formula is not valid")

    def entailBelief(self):
        while True:
            try:
                formula = input("Insert the formula: ")
                result = PL_Resolution(self.bb.getclauses(), to_cnf(formula))
                print("The belief base does{} entail {}".format({True: "", False: " not"}[result], formula))
                break
            except SympifyError:
                print("The formula is not valid")


def main():
    ui = UserInterface()
    ui.run()


main()
