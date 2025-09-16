def PSTC_specification(n, number):
    exp_probs = [0] * (2 ** n)
    exp_probs[number] = 1
    return exp_probs

def MSTC_specification(input_probs):
    return input_probs