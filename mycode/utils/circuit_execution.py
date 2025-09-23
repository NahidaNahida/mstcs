from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def circuit_execution(qc: QuantumCircuit, shots: int) -> dict:
    """
    Execute a quantum circuit and return the measurement results as a dictionary.

    This function simulates the execution of a quantum circuit on the 
    Qiskit Aer ``qasm_simulator`` backend. The circuit is transpiled 
    for the backend, executed for the specified number of shots, and 
    the resulting measurement outcomes are returned as integer-labeled 
    counts.

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to be executed. The circuit should contain 
        measurement operations to produce classical outcomes.
    shots : int
        Number of repetitions for circuit execution. A larger number 
        of shots yields more accurate probability estimates of the 
        measurement outcomes.

    Returns
    -------
    dict
        A dictionary mapping computational basis states (as integers) 
        to the number of times each state was measured. The keys are 
        integers representing bitstrings (little-endian convention).
    """
    backend = Aer.get_backend('qasm_simulator')
    executed_circuit = transpile(qc, backend)
    count= backend.run(executed_circuit, shots=shots).result().get_counts()
    dict_counts = count.int_outcomes()
    return dict_counts