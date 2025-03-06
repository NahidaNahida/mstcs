import math
import numpy as np

def PSTC_specification(n, number, slop, offset, domain, image):
    a, b = domain[0], domain[1] 
    c, d = image[0], image[1] 
    slopm = slop * (b - a) / (2 ** n - 1) / (d - c)
    offsetm = (offset - c) / (d - c)
    theta = np.pi * (slopm * number + offsetm)
    
    res_vec = [math.cos(theta / 2), math.sin(theta / 2)] 
    exp_probs = [res_vec[0] ** 2, res_vec[1] ** 2]
    return exp_probs

def MSTC_specification(n, numbers, inputProbs, slop, offset, domain, image):
    exp_probs = [0, 0]
    a, b = domain[0], domain[1] 
    c, d = image[0], image[1] 
    slopm = slop * (b - a) / (2 ** n - 1) / (d - c)
    offsetm = (offset - c) / (d - c)
    for number in numbers:
        theta = np.pi * (slopm * number + offsetm)
        exp_probs[0] += inputProbs[number] * math.cos(theta / 2) ** 2
        exp_probs[1] += inputProbs[number] * math.sin(theta / 2) ** 2
    return exp_probs