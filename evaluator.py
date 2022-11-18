#!/usr/bin/env python
'''
Code written by Erwin de Wolff
for the course
Theoretical Modelling for Cognitive Science
at Radboud University
Date - November 2022
'''

import matplotlib.pyplot as plt

def calculate_coherence(graph, accepted, rejected):
    # Unpack graph
    (elements, c_plus, c_minus,
     discriminating, foundational) = graph
    
    coherence = 0
    # Sum weights of met positive constraints
    for (e1, e2, w) in c_plus:
        if ((e1 in accepted and e2 in accepted) or
            (e1 in rejected and e2 in rejected)):
            coherence += w

    # Sum weights of met negative constraints
    for (e1, e2, w) in c_minus:
        if ((e1 in accepted and e2 in rejected) or
            (e1 in rejected and e2 in accepted)):
            coherence += w

    # If any discriminating elements are given
    # and accepted, their coherence is added
    for (e,w) in discriminating:
        if e in accepted:
            coherence += w

    # If any elements are foundational but
    # are not accepted, negative coherence is given
    # This guarantees that it is not the best assignment
    for e in foundational:
        if e not in accepted:
            coherence = -1

    return round(coherence,2)



def get_structure_similarity(optimal_assignments,
                             assignment):
    (accepted, rejected) = assignment

    highest_struct_approx = 0
    n = len(accepted)+len(rejected)
    for (opt_accepted, opt_rejected) in optimal_assignments:
        struct_approx = 0
        
        # Increase structure similarity
        # For each matching accepted element
        for e in opt_accepted:
            if e in accepted:
                struct_approx += 1/n

        # Increase structure similarity
        # For each matching rejected element
        for e in opt_rejected:
            if e in rejected:
                struct_approx += 1/n

        # Given multiple optimal solutions
        # return the highest structure similarity
        if struct_approx > highest_struct_approx:
            highest_struct_approx = struct_approx
            
    return highest_struct_approx



def print_assignments(model_name, assignments, coherence):
    # Print the found solution
    # This function is only called in main_custom.py
    for i, (accepted, rejected) in enumerate(assignments):
        if len(assignments) > 1:
            line = f"{model_name} Solution {i+1}" 
        else:
            line = f"{model_name} Solution"

        print(line)
        print("".join(["-" for _ in line]))
        print(f"Accepted:  {accepted}")
        print(f"Rejected:  {rejected}")
        print(f"Coherence: {coherence}\n\n")



def save_results(nr_elements, algorithm_names, epochs,
                 value_similarities, structure_similarities,
                 show=False, colors=['b', 'orange', 'g', 'r']):
    legend_list = []
    
    plt.figure(figsize=(12.8,7.2))
    plt.title(f"Similarity To Optimal given N ({epochs} Simulations)")

    # For each model used, draw a dotted line for the
    # structure similarity, and a full line for the
    # value similarity
    for i in range(len(value_similarities)):
        plt.plot(nr_elements, value_similarities[i],
                 c=colors[i])
        plt.plot(nr_elements, structure_similarities[i],
                 '--', c=colors[i])

        # Annote each point
        for x, y1, y2 in zip(nr_elements,
                             value_similarities[i],
                             structure_similarities[i]):
            if (y1 > y2):
                plt.text(x-0.1, y1+0.01, str(round(y1,2)), c=colors[i])
                plt.text(x-0.1, y2-0.04, str(round(y2,2)), c=colors[i])
            else:
                plt.text(x-0.1, y1-0.04, str(round(y1,2)), c=colors[i])
                plt.text(x-0.1, y2+0.01, str(round(y2,2)), c=colors[i])

        legend_list += [f"Value       ({algorithm_names[i]})",
                        f"Structure ({algorithm_names[i]})"]

    plt.ylim([0,1.05])
    plt.xlabel("Nr. Elements")
    plt.ylabel("Similarity (%)")
    plt.legend(legend_list)
    plt.xticks(nr_elements)
    plt.yticks([0.1*i for i in range(11)])

    if (show):
        plt.show()
    else:
        plt.savefig("Result_graph.png",dpi=150)

