def PSTC_specification(n: int, number: int, L: int, sign: bool) -> list[int]:
    exp_probs = [0] * (2 ** n)
    if sign == True:
        exp_probs[int(number >= L)] = 1
    else:
        exp_probs[int(number < L)] = 1
    return exp_probs

def MSTC_specification(numbers: list[int], probs: list[float], L: int, sign: bool) -> list[float]:
    exp_probs = [0.0] * (len(numbers))    # [p(0), p(1)]
    for number in numbers:
        if sign == True:
            exp_probs[int(number >= L)] += probs[number]
        else:
            exp_probs[int(number < L)] += probs[number]
    return exp_probs
    