import numpy as np
import math, cmath

def PSTC_specification(n, number, if_swap):
    for index in range(n):
        theta = 2 * math.pi * number / (2 ** (index + 1))
        tempVec = 1 / math.sqrt(2) * np.array([1, cmath.exp(theta * 1j)])
        if index == 0:
            stateVec = tempVec
        else:
            if if_swap:
                stateVec = np.kron(stateVec, tempVec)
            else:
                stateVec = np.kron(tempVec, stateVec)
    exp_probs = (abs(stateVec) ** 2).tolist()
    return exp_probs

def MSTC_specification(numbers, input_probs, n, if_swap):
    exp_probs = np.array([0] * (2 ** n))
    for number in numbers:
        cond_probs = PSTC_specification(n, number, if_swap)
        add_probs = np.array(cond_probs) * input_probs[number]
        exp_probs = exp_probs + add_probs
    return exp_probs