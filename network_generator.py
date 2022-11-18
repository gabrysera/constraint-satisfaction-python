#!/usr/bin/env python
'''
Code written by Erwin de Wolff
for the course
Theoretical Modelling for Cognitive Science
at Radboud University
Date - November 2022
'''

from random import random, choice

def generate_random_graph(nr_elements,
                          p_c_plus, p_c_minus,
                          p_discr, p_found,
                          min_value=1, max_value=1):

    # Check for proper parameter settings. Will raise error
    # if input parameters are not allowed
    assert p_c_plus <= 1 and p_c_plus >= 0, f"\np_c_plus must lie between 0 and 1 (both inclusive): input is {p_c_plus}"
    assert p_c_minus <= 1 and p_c_minus >= 0, f"\np_c_minus must lie between 0 and 1 (both inclusive): input is {p_c_minus}"
    assert p_discr <= 1 and p_discr >= 0, f"\np_discr must lie between 0 and 1 (both inclusive): input is {p_discr}"
    assert p_found <= 1 and p_found >= 0, f"\np_found must lie between 0 and 1 (both inclusive): input is {p_found}"
    assert p_c_plus + p_c_minus > 0, f"\nAt least p_c_plus or p_c_minus must have a positive probability"
    assert p_discr * p_found == 0, f"\nThe set of elements cannot have discriminating *and* foundational elements\nSet either p_discr or p_found to 0"
    assert min_value <= max_value, f"\nThe minimum weight of a constraint cannot be bigger than the maximum weight: given range is [{min_value},{max_value}]"
    assert min_value > 0 and max_value > 0, f"\nThe weights of constraints must be positive: given range is [{min_value},{max_value}]"
    
    # Create simple elements
    elements = []
    for i in range(nr_elements):
        elements += [f"E{i+1}"]

    # Randomly add positive or negative costraints
    # Two elements can only have one constraint, and
    # a constraint is added with probabilities p_c_plus
    # for positive constraints, and p_c_minus for negative
    # constraints.
    c_plus = []
    c_minus = []
    for i in range(len(elements)):
        for j in range(i+1,len(elements)):
            e1 = elements[i]
            e2 = elements[j]
            p = random()
            if p <= p_c_plus:
                coh = min_value+round((max_value-min_value)*random(),2)
                c_plus += [(e1,e2,coh)]
            elif (p - p_c_plus <= p_c_minus):
                coh = min_value+round((max_value-min_value)*random(),2)
                c_minus += [(e1,e2,coh)]

    # If random adding did not create any constraints
    # one constraint is added. This is constraint is
    # positive if p_c_plus > 0, and negative otherwise.
    # The value of this constraint is the minimum value.
    if (len(c_plus) == 0 and len(c_minus) == 0):
        if (p_c_plus > 0):
            c_plus.append((elements[0], elements[1], min_value))
        else:
            c_minus.append((elements[0], elements[1], min_value))

    # Randomly add elements to the discriminating set
    # with probability p_discr
    discriminating = []
    for e in elements:
        if random() <= p_discr:
            coh = min_value+round((max_value-min_value)*random(),2)
            discriminating += [(e,coh)]

    # If random adding did not create any discriminating constraints
    # but p_discr > 0, add 1 such constraint with minimal value
    if (len(discriminating) == 0 and p_discr > 0):
        discriminating += [(choice(elements), min_value)]

    # Randomly add elements to the foundational set
    # with probability p_found
    foundational = []
    for e in elements:
        if random() <= p_found:
            foundational += [e]

    # If random adding did not create any foundational constraints
    # but p_found > 0, add 1 such constraint
    if (len(foundational) == 0 and p_found > 0):
        foundational += [choice(elements)]

    return (elements, c_plus, c_minus, discriminating, foundational)
