from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def circuit_execution(qc: QuantumCircuit, shots: int) -> dict:
    """
        Execute the quantum circuit with given shots, and then return the measurement results.
    """
    backend = Aer.get_backend('qasm_simulator')
    executed_circuit = transpile(qc, backend)
    count= backend.run(executed_circuit, shots=shots).result().get_counts()
    dict_counts = count.int_outcomes()
    return dict_counts