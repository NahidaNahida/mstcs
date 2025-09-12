import math

def PSTC_specification(number, slope, offset):
    expProbs = [0, 0]
    a, b = slope / 2, offset / 2
    expProbs[0] = math.cos(a * number + b) ** 2
    expProbs[1] = math.sin(a * number + b) ** 2
    return expProbs

def MSTC_specification(numbers, inputProbs, slope, offset):
    expProbs = [0, 0]   # [p(0), p(1)]
    a, b = slope / 2, offset / 2
    for number in numbers:
        expProbs[0] += inputProbs[number] * math.cos(a * number + b) ** 2
        expProbs[1] += inputProbs[number] * math.sin(a * number + b) ** 2
    return expProbs