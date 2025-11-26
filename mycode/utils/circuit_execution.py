from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def circuit_execution(qc: QuantumCircuit, shots: int) -> dict:
    """
    Execute a quantum circuit on the backend and return the measurement 
    results as a dictionary.

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

if __name__ == "__main__":
    """
    Unit testing. 
    Run:
        python mycode/utils/circuit_execution.py
    """
    # ----------------------------
    # Test inputs 
    # ----------------------------

    def test_input_0():
        # Create a circuit containing a composite gate  
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure(0, 0)
        qc.measure(1, 1)     
        return qc

    # ----------------------------
    # Unit tests 
    # ----------------------------

    def unit_test_0(qc, shots):
        dict_counts = circuit_execution(qc, shots)
        assert isinstance(dict_counts, dict)

    # ----------------------------
    # Results needing manual check 
    # ----------------------------

    def manual_check_0(qc, shots):
        dict_counts = circuit_execution(qc, shots)
        print(dict_counts)

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {"input": test_input_0, "shots": 1024, "function": unit_test_0},
        "1": {"input": test_input_0, "shots": 1024, "function": manual_check_0},
    }
    for id, execution_dict in executed_test.items():
        print(f"test_id={id}:")
        test_input = execution_dict["input"]()
        shots = execution_dict["shots"]
        try:
            execution_dict["function"](test_input, shots)
            if "manual" in execution_dict["function"].__name__:
                print("need manual check")
            else:
                print("pass")
        except AssertionError as e:
            print("fail")
            raise