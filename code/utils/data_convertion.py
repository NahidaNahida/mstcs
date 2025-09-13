import numpy as np

def generate_numbers(n: int, m: int):
    '''
        Generate all the n-digit m-ary numbers and store them at corresponding lists

        Input variables:
            + n:        the number of target qubits
            + m:        the number of control qubits
        
        Output variable:
            + number_list: the list of all the possible values
        
        Example: 
            + Input: n = 3, m = 2
            + Output: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
    '''

    if n <= 0:
        return [[]]                     # return an empty list

    if n == 1:
        return [[i] for i in range(m)]  # generate 1-digit m-ary numbers

    # recursion
    smaller_numbers = generate_numbers(n - 1, m)
    number_list = []
    for digit in range(m):
        for smaller_number in smaller_numbers:
            number_list.append([digit] + smaller_number)

    return number_list

def output_prob(counts, n):
    
    """
        The list of measurement results is transformed into corresponding probability
        distribution (or frequencies)

        Input variables:
            + counts  [class]   the execution outputs directly derived from Qiskit backend
            + n       [int]     the number of qubits

        Output variable:
            + prob_dist [array] the probability distribution of outputs
    
    """

    output_dic = counts.int_outcomes()
    prob_dist = []
    for i in range(2**n):
        if i not in output_dic:
            prob_dist.append(0)
        else:
            prob_dist.append(output_dic[i]/counts.shots())
    prob_dist = np.asarray(prob_dist) / np.sum(prob_dist)
    return prob_dist