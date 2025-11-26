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

if __name__ == "__main__":
    """
    Unit testing.
    Run:
        python mycode/utils/circuit_complexity_measure.py
    """

    # ------------------------
    # Test inputs
    # ------------------------

    def test_input_0():
        # Create a circuit containing a composite gate  
        qc = QuantumCircuit(1)
        qc.h(0)       
        return qc

    # ------------------------
    # Integration Tests
    # ------------------------

    def integration_test_0(qc):
        decomposed = full_circuit_decomposition(qc)

        # Should not contain the "h" gate anymore after decomposition
        assert "h" not in decomposed.count_ops().keys()

    def integration_test_1(qc):
        decomposed = full_circuit_decomposition(qc)
        # The resulting circuit should still be functionally equivalent in qubit count
        assert qubit_count(decomposed) == 1

    def integration_test_2(qc):
        decomposed = full_circuit_decomposition(qc)
        # The decomposed gates and depths should be no less than 1
        assert gate_count(decomposed) >= 1
        assert depth_count(decomposed) >= 1

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {"input": test_input_0, "function": integration_test_0},
        "1": {"input": test_input_0, "function": integration_test_1},
        "2": {"input": test_input_0, "function": integration_test_2},
    }

    for id, execution_dict in executed_test.items():
        print(f"test_id={id}:")
        test_input = execution_dict["input"]()
        try:
            execution_dict["function"](test_input)
            print("pass")
        except AssertionError as e:
            print("fail")
            raise