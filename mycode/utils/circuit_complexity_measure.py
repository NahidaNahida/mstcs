"""
This module provides utility functions for analyzing and processing Qiskit quantum circuits
to measure their structural complexity.

It includes methods to:
- Recursively decompose a circuit into basis gates.
- Compute the depth (longest path of operations).
- Count the total number of gates.
- Count the number of qubits.

These metrics are commonly used in quantum algorithm analysis to evaluate 
resource requirements and optimize circuit designs.
"""

from qiskit import QuantumCircuit

def full_circuit_decomposition(qc: QuantumCircuit) -> QuantumCircuit:
    """
    Recursively decomposes a quantum circuit until only basis gates remain.

    Args:
        qc (QuantumCircuit): The quantum circuit to decompose.

    Returns:
        QuantumCircuit: A fully decomposed circuit containing only basis gates.
    """
    while True:
        # Decompose one level of the circuit
        decomposed_qc = qc.decompose()
        # Stop when decomposition does not change the circuit
        if decomposed_qc == qc:
            break
        qc = decomposed_qc
    return qc

def depth_count(qc: QuantumCircuit) -> int:
    return qc.depth()

def gate_count(qc: QuantumCircuit) -> int:
    gate_dict = qc.count_ops()  # Returns a dictionary {gate_name: count}
    return sum(gate_dict.values())

def qubit_count(qc: QuantumCircuit) -> int:
    return qc.num_qubits