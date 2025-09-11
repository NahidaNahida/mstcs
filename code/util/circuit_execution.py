from qiskit import transpile
from qiskit_aer import Aer

def circuit_execution(qc, shots):
    """
        Execute the quantum circuit with given shots, and then return the measurement results.
    """
    backend = Aer.get_backend('qasm_simulator')
    executedQC = transpile(qc, backend)
    count= backend.run(executedQC, shots=shots).result().get_counts()
    dict_counts = count.int_outcomes()
    return dict_counts