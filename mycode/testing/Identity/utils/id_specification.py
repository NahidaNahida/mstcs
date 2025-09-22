def PSTC_specification(n: int, number: int) -> list[int]:
    exp_probs = [0] * (2 ** n)
    exp_probs[number] = 1
    return exp_probs

def MSTC_specification(input_probs: list[float]) -> list[float]:
    return input_probs