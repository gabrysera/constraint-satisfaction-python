#!/usr/bin/env python
'''
Code written by Erwin de Wolff
for the course
Theoretical Modelling for Cognitive Science
at Radboud University
Date - November 2022
'''

from coherence_algorithms import *
from evaluator import *

'''
    BELIEF NETWORK DEFINITION
'''
# Define the elements
elements = ["A","B","C"]

# Define any postive constraints
# in the format (e1, e2, w(e1,e2))
c_plus =   [("A", "C", 1)]

# Define any negative constraints
# in the format (e1, e2, w(e1,e2))
c_minus =  [("A", "B", 1),
            ("B", "C", 1)]

# Define any discriminating elements
# and the coherence for accepting them
# in the format (d, w(d))
discriminating = [("A", 2)]
#discriminating = []

# Define any foundational elements
#foundational = ["B"]
foundational = []




'''
    SET CONNECTIONIST ALGORITHM PARAMETERS
''' 
epsilon = 10**-10       # The connectionist algorithm terminates
                        # When the difference is unit activation
                        # is no more than epsilon
decay = 0.05            # The activation of each unit is reduced by
                        # decay during each update
max_epochs = 200        # After this many epochs, the connectionist
                        # algorithm will terminate, regardless of
                        # the change in activation at that time



'''
    INFERENCE AND EVALUATION
'''
graph = (elements, c_plus, c_minus, discriminating, foundational)

# Step 1: Get the optimal truth assignment
# and corresponding coherence value through
# the exhaustive algorithm
optimal_assignments, optimal_coherence = find_exhaustive_coherence(graph)

# Step 2: Get the truth assignment
# and corresponding coherence value through
# the harmony-maximisation algorithm
harmony_assignment, harmony_coherence = find_connectionist_coherence(graph, epsilon, decay, max_epochs)

# Output the truth assignment(s) that lead to
# the maximal coherence
print_assignments("Exhaustive", optimal_assignments, optimal_coherence)
print_assignments("Connectionist", [harmony_assignment], harmony_coherence)

structure_similarity = get_structure_similarity(optimal_assignments, harmony_assignment)

# Return the ratio of the estimated coherence and the maximal coherence 
print(f"Value Similarity: {harmony_coherence/optimal_coherence} ({harmony_coherence}/{optimal_coherence})")
print(f"Structure Similarity: {structure_similarity} ({int(len(elements)*structure_similarity+0.5)}/{len(elements)})")





