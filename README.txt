This python project is designed to analyse the effect of different parameters on the value and structure similarity 
between an optimal (exhaustive) truth assignment over a coherence model, and the connectionist algorithm as 
proposed by Thagard & Verbeurgt (1998).

#######################
#  USING THE PROGRAM  #
#######################

To gather data of a particular simulation, modify and run either of the two following files:

- main_custom.py:
	In this file, users can define a specific coherence network. This is done by defining the elements, 
	the positive constraints between elements (and their weight), and the negative constraint (and their weight). 
	Users can also set the different parameters used by the connectionist algorithm.
	
	Users can make particular elements discriminating by making a list containing tuples (element, weight). 
	This indicates how much coherence is added to an assignment where the element is accepted.
	
	Users can make particular elements foundational by making a list of elements. 
	Each element in this list is assumed (or forced) to be accepted at all times. 
	In the connectionist case, this means that the associated unit is fixed to activation value 1.
	
	The file contains an example graph. When running the file, the optimal (exhaustive) assignment(s) of the 
	coherence network will be outputted, along with the solution given by the connectionist algorith. In addition, 
	the connectionist assignment will be compared to the optimal solution to determine the value similarity and 
	(highest) structure similarity.



- main_random.py:
	In this file, users can define a set of parameters to generate random coherence networks with. The program 
	will then generate a number of such networks (as given by the parameter epochs, set by the user), and compare 
	the optimal solution with a random (baseline) and the connectionist solution. It will do so for different sizes 
	of the coherence network, as given by the parameters min_n and max_n. 
	
	The average value and structure similarities per network size across the epochs will be outputted to a graph file 
	called result_figure.png.
	
	IMPORTANT: The program will update the result_figure.png file after each series of simulations of a particular 
	size n. As such, you can safely terminate the program mid-run without throwing away your results so far. 
	If, for example, the program is still calculating the solutions for coherence networks of n=20, 
	result_figure.png will already contain the results for n=19.



#########################
#  EDITING THE PROGRAM  #
#########################

Although the code was tested and designed to match the implementation details as closely as possible, it is possible
that you would like to make changes to the code. To do so, here is an overview of the remaining files.

- coherence_algorithms.py:
	This file contains all the coherence-maximising algorithms used by the program. There are three algorithms:
		- A random algorithm that accepts and rejects elements with equal probability (unless the element is foundational, 
		  in which case it always accepts them).
		- An exhaustive algorithm that find the truth assignment that maximises the coherence value.
		- A connectionist algorithm that incremently updates until it converges to a stable state. If this is not 
		  reached, the program will eventually terminate. Then, the unit activation is translated to acceptance/rejection, 
		  and the results coherence value is calculated.
		
	Users can add/modify algorithms easily, provided that some things are ensured:
		- The algorithm takes (at least) a graph as input
		- The algorithm return one or multiple truth assignments and the corresponding coherence value.



- evaluator.py:
	This file contains multiple useful functions to evaluating solutions. These are:
		- calculate_coherence, which takes a coherence network and the accepted and rejected elements and returns the coherence.
		- get_structure_similarity, which determines the structure similarity between a (set of) optimal truth assignment(s)
		  and another truth assignment.
		- print_assignments, which output the truth assignment found by one of the coherence maximising algorithms.
		- save_results, which compiles all the similarities of the tested algorithms (compared to the optimal solution) 
		  into a image called result_figure.png.
	
	

- network_generator.py:
	This file defines how a random coherence network is generated. It does by randomly creating constraints between elements.
	
	While generating, the algorithm will:
		- Make sure that only elements that do not have a constraint yet can be given a constraint.
		- Ensure that at least one constraint is given. The type of constraint depends on the set parameters.
		- Ensure that at least one element will have a discriminating value, given that p_discr > 0. 
		- Ensure that at least one element is foundational, given that p_found > 0.
	
	It will not:
		- Check whether each element is connected to at least one other element.
		- Check whether the coherence network exists of two or more unconnected sub-graphs.
		- Check whether the optimal coherence will ever be higher than zero (although this is dealt with when determining 
		  value similarity).
		- Other potential issues missed by the programmer.
		

Code written and tested by Erwin de Wolff, November 2022