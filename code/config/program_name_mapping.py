FULL2ABB_MAPPING = {
    "Identity": "id",
    "IntegerComparator": "comp",
    "LinearAmplitudeFunction": "amplitude",
    "LinearPauliRotations": "pauli",
    "QuadraticForm": "quad",
    "QuantumFourierTransform": "qft",
    "WeightedAdder": "adder"
}

# Generate reverse mapping
ABB2FULL_MAPPING = {v: k for k, v in FULL2ABB_MAPPING.items()}