#!/usr/bin/env python
'''
Code written by Erwin de Wolff
for the course
Theoretical Modelling for Cognitive Science
at Radboud University
Date - November 2022
'''

from random import random
from evaluator import calculate_coherence

def find_random_coherence(graph):
    # Unpack graph
    elements = graph[0]
    foundational = graph[4]
    
    accepted = []
    rejected = []

    # Randomly add elements to accepted or rejected
    # (foundational elements are always accepted)
    for e in elements:
        if e in foundational or random() <= 0.5:
            accepted.append(e)
        else:
            rejected.append(e)

    # Determine coherence of truth assignment
    # and return solution 
    coherence = calculate_coherence(graph, accepted, rejected)
    return (accepted, rejected), coherence



def find_exhaustive_coherence(graph, accepted=[],
                              rejected=[], index=0):
    # Grab elements from graph
    elements = graph[0]
    foundational = graph[4]
    
    # If all elements have been accepted or rejected
    if (index >= len(elements)):
        # Calculate the coherence of the current assignment
        coherence = calculate_coherence(graph, accepted, rejected)
        return [(accepted, rejected)], coherence

    # Else, try all remaining combinations of accepted/rejected
    else:
        # Get the next element for consideration
        element = elements[index]

        # If the considered element is foundational, always accept it
        if element in foundational:
            return find_exhaustive_coherence(graph, accepted+[element],
                                             rejected, index+1)

        # Recursive go through all options where element is accepted
        left_branch, coh1 = find_exhaustive_coherence(graph, accepted+[element],
                                                      rejected, index+1)

        # Recursive go through all options where element is rejected
        right_branch, coh2 = find_exhaustive_coherence(graph, accepted,
                                                       rejected+[element], index+1)

        # If accepting or rejecting made no difference
        if coh1 == coh2:
            return left_branch + right_branch, coh1

        # If accepting led to a higher coherence than rejecting
        elif coh1 > coh2:
            return left_branch, coh1

        # If rejecting led to a higher coherence than accepting
        else:
            return right_branch, coh2



def update_units(units, weights, decay,
                 found_indices, discr_units, discr_weights):
    new_units = [unit for unit in units]
    for x, unit1 in enumerate(new_units):
        # If unit is foundational, leave at 1
        if x in found_indices:
            new_units[x] = 1

        else:
            # Calculate the net activation of the unit
            net = 0
            # Add activation caused by other units
            for y, unit2 in enumerate(new_units):
                net += weights[x][y] * unit2

            # Add activation caused by discriminating units
            for y, discr_unit in enumerate(discr_units):
                net += discr_weights[x][y]

            # Update the unit
            if net > 0:
                new_units[x] = unit1*(1-decay) + net*(1-unit1)
            else:
                new_units[x] = unit1*(1-decay) + net*(unit1+1)

    # Return the new unit activations pushed within bounds
    return [max(-1,min(1, unit)) for unit in new_units]
            


def find_connectionist_coherence(graph, epsilon=0.001,
                                 decay=0.05, max_epochs=200):
    # Unpack graph
    (elements, c_plus, c_minus,
     discriminating, foundational) = graph

    # Transform elements and constraints
    # into units and weights
    units = [0.01 for _ in elements]
    weights = [[0 for _ in units] for _ in units]

    # Create discriminating elements
    discr_units = [1 for _ in discriminating]
    discr_weights = [[0 for _ in discr_units] for _ in units]
    for j, (e, w) in enumerate(discriminating):
        i = elements.index(e)
        discr_weights[i][j] = w

    # Get the foundational indices
    # so these can be set to 1
    found_indices = [elements.index(f) for f in foundational]
    
    # Create a positive weight
    # for each positive constraint
    for (e1, e2, w) in c_plus:
        x = elements.index(e1)
        y = elements.index(e2)
        weights[x][y] = w
        weights[y][x] = w

    # Create a negative weight
    # for each negative constraint
    for (e1, e2, w) in c_minus:
        x = elements.index(e1)
        y = elements.index(e2)
        weights[x][y] = -w
        weights[y][x] = -w

    # Update the units until stable
    # or a set number of iterations
    # has passed.
    change = 1
    count = 0
    while change > epsilon and count < max_epochs:
        new_units = update_units(units, weights, decay,
                                 found_indices, discr_units,
                                 discr_weights)
        change = sum([abs(u1-u2) for u1,u2 in zip(units, new_units)])
        units = [u for u in new_units]
        count += 1
        
    # Accept all elements with a positive
    # activation, and reject all those with
    # a negative activation.
    accepted = []
    rejected = []
    for e, u in zip(elements, units):
        if u > 0:
            accepted.append(e)
        else:
            rejected.append(e)

    # Determine coherence of truth assignment
    # and return solution
    coherence = calculate_coherence(graph, accepted, rejected)        
    return (accepted, rejected), coherence
