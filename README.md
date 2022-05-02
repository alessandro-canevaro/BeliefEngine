
# BeliefEngine
Belief Revision is the project for the course Introduction to AI, which is implemented using python programming language.

# General Description
Our Belief Engine has Class BeliefBase which is the foundation of the whole implementation, which stores and handles all the beliefs of the agent.
- main.py - This is the entry point for the project which includes the user interface.
- BeliefBase.py - The heart of the project, which includes key function such as contraction, revision etc.
- Resolution.py - handles the logical entailments properties
- agmtest.py - includes different AGM postulates test functions

# Packages required to install prior to run the game
- pip install sympy

# Key actions to be performed:

Print(p): Print current belief base
Add(a): Add a new belief
Revise(r): Revise the current belief base with a new belief
Contraction(c): Contract the current belief base
Check(e): Check if a formula is entailed in the belief base
Clear(w): Clear current belief base
Quit(q): Terminate execution

# Test
Run the AGM postulates test 
- python agmtest.py
