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
from network_generator import generate_random_graph
from time import time

'''
    PARAMETERS FOR NETWORK GENERATION
'''
# Probability that two elements will have a
# positive or negative constraint between them
# These values must sum to 1 at most
p_c_plus = 0.25
p_c_minus = 0.25

# Probability that an element will be either
# discriminating or foundational
# Only one parameter can be positive
p_discr = 0.1
p_found = 0.0

# The minimum and maximum values of a constraint
min_weight = 1
max_weight = 10

# The minimum and maximum size of the belief
# networks. Give at least 2 elements
min_n = 2
max_n = 15



'''
    SET CONNECTIONIST ALGORITHM PARAMETERS
'''
# The connectionist algorithm terminates
# When the difference is unit activation
# is no more than epsilon
epsilon = 10**-10

# The activation of each unit is reduced by
# decay during each update
decay = 0.05

# After this many epochs, the connectionist
# algorithm will terminate, regardless of
# the change in activation at that time
max_epochs = 200


'''
    RUN SIMULATIONS PARAMETERS AND RUN
'''
# How many simulations per size of n you want to run
epochs = 1000

# Collect simulation data
ns = [n for n in range(min_n, max_n+1)]
value_similarities = [[], []]
structure_similarities = [[], []]

print("Comparing coherence values for...")
for n in ns:
    # Initialize results for n
    value_similarities[0].append(0)
    structure_similarities[0].append(0)
    value_similarities[1].append(0)
    structure_similarities[1].append(0)
    
    print(f"n={n}", end='')
    start = time()
    for _ in range(epochs):
        # Generate random graph
        graph = generate_random_graph(n, p_c_plus, p_c_minus,
                                      p_discr, p_found,
                                      min_weight, max_weight)

        # Get optimal solution (exhaustive)
        optimal_assignments, optimal_coherence = find_exhaustive_coherence(graph)


        ##################################
        # Get random (baseline) solution #
        ##################################
        assignment, coherence = find_random_coherence(graph)

        # Update value similarity of random algorithm
        if optimal_coherence == 0:
            value_similarity = 1
        else:
            value_similarity = (coherence/optimal_coherence)
        value_similarities[0][n-min_n] += (value_similarity/epochs)

        # Update structure similarity of random algorithm
        structure_similarity = get_structure_similarity(optimal_assignments, assignment)
        structure_similarities[0][n-min_n] += (structure_similarity/epochs)



        ##############################
        # Get connectionist solution #
        ##############################
        assignment, coherence = find_connectionist_coherence(graph, epsilon,
                                                             decay, max_epochs)

        # Update value similarity of connectionist algorithm
        if optimal_coherence == 0:
            value_similarity = 1
        else:
            value_similarity = (coherence/optimal_coherence)
        value_similarities[1][n-min_n] += (value_similarity/epochs)

        # Update structure similarity of connectionist algorithm
        structure_similarity = get_structure_similarity(optimal_assignments, assignment)
        structure_similarities[1][n-min_n] += (structure_similarity/epochs)


    # Update result graph and output time spend on size n
    print(f", done in {round(time()-start,2)} seconds")
    save_results(ns[0:n-min_n+1], ["Random", "Connectionist"], epochs,
                 value_similarities, structure_similarities)












