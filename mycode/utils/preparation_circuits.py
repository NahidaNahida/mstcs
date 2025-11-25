import math
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import RYGate 
from qiskit import QuantumCircuit
import numpy as np

from .circuit_execution import circuit_execution

def separable_control_state_preparation(theta_list: list[float]) -> QuantumCircuit:
    """
    Prepare separable (product) control states based on a list of rotation angles.

    Each control qubit is initialized independently with a single-qubit rotation:
        |ψ(θ)> = cos(θ/2)|0> + sin(θ/2)|1>

    The overall control state is the tensor product of all such single-qubit states,
    making the result fully separable.

    Parameters
    ----------
    theta_list : list[float]
        A list of rotation angles, one for each control qubit.

    Returns
    -------
    QuantumCircuit
        A quantum circuit with m qubits (m = len(theta_list)), where each qubit
        has an Ry rotation applied according to its corresponding angle.

    Example
    -------
    >>> theta_list = [math.pi / 2, math.pi / 2]
    >>> qc = separable_control_state_preparation(theta_list)
    >>> print(qc)

    Example circuit::
             ┌─────────┐
    q_0: ────┤ Ry(π/2) ├
             ├─────────┤
    q_1: ────┤ Ry(π/2) ├
             └─────────┘
    """
    m = len(theta_list)
    qc = QuantumCircuit(m)

    for index, theta in enumerate(theta_list):
        # Apply an Ry rotation to prepare each qubit in |ψ(θ)>
        qc.ry(theta, index)

    return qc


def separable_control_state_probs(theta_list: list[float]) -> list[float]:
    """
    Compute the output probability distribution for a separable control-state preparation.

    Each qubit is initialized in a state determined by a single rotation angle θ,
    where the state vector is defined as:

        |ψ(θ)> = cos(θ/2)|0> + sin(θ/2)|1>

    The final separable state is obtained by taking the tensor product of all 
    single-qubit states, and the output probability distribution corresponds 
    to the squared amplitudes of the resulting state vector.

    Parameters
    ----------
    theta_list : list[float]
        A list of rotation angles, one for each control qubit.

    Returns
    -------
    list[float]
        A probability distribution over computational basis states. The length
        of the list is 2^m, where m = len(theta_list).

    Example
    -------
    >>> theta_list = [math.pi/2, math.pi/3]
    >>> separable_control_state_probs(theta_list)
    [0.375, 0.125, 0.375, 0.125]
    """
    for index, theta in enumerate(theta_list):
        # State vector of a single qubit after rotation Ry(theta)
        temp_state = np.array([math.cos(theta / 2), math.sin(theta / 2)])

        if index == 0:
            # Initialize the composite state with the first qubit
            final_state = temp_state
        else:
            # Tensor product: add this qubit to the existing system
            final_state = np.kron(temp_state, final_state)

    # Probabilities = squared amplitudes of the final state
    output_probs = final_state ** 2
    return output_probs.tolist()

def entangled_control_state_preparation(theta_list: list) -> QuantumCircuit:
    """
    Prepare an entangled control state according to the given rotation angles.

    Parameters
    ----------
    theta_list : list[float]
        A list of (2^m - 1) angles for RY rotation gates, where `m` is the
        number of control qubits.

    Returns
    -------
    QuantumCircuit
        A quantum circuit that prepares the desired entangled control state.

    Example
    -------
    >>> theta_list = [2 * math.pi / 3, math.pi / 6, math.pi / 3]
    >>> qc = entangled_control_state_preparation(theta_list)
    >>> print(qc)

    Example circuit::

         ┌──────────┐┌───┐           ┌───┐
    q_0: ┤ Ry(2π/3) ├┤ X ├─────■─────┤ X ├─────■─────
         └──────────┘└───┘┌────┴────┐└───┘┌────┴────┐
    q_1: ─────────────────┤ Ry(π/6) ├─────┤ Ry(π/3) ├
                          └─────────┘     └─────────┘
    """

    def processed_qubits(decimal_num, bits):
        """
        Convert a decimal number into a binary string of length `bits`,
        and return the positions of the zero-bits (LSB = index 0).
        """
        binary_str = bin(decimal_num)[2:].zfill(bits)
        return [i for i, digit in enumerate(binary_str[::-1]) if digit == "0"]

    # Determine the number of control qubits m from the length of theta_list
    m = int(math.log2(len(theta_list) + 1))
    qc = QuantumCircuit(m)

    theta_index = 0
    for i in range(m):
        if i == 0:
            # First qubit: apply a single RY rotation
            qc.ry(theta_list[theta_index], 0)
            theta_index += 1
        else:
            qubit_index_i = list(range(i + 1))  # indices of the first (i+1) qubits
            for j in range(2**i):
                qubit_index_j = processed_qubits(j, i)

                # If some qubits correspond to '0', apply X gates before/after control
                if qubit_index_j:
                    qc.x(qubit_index_j)
                    qc.append(RYGate(theta_list[theta_index]).control(i), qubit_index_i)
                    qc.x(qubit_index_j)
                else:
                    qc.append(RYGate(theta_list[theta_index]).control(i), qubit_index_i)

                theta_index += 1

    return qc

def circuit_test(qc: QuantumCircuit, shots: int) -> dict:
    """
    Execute a quantum circuit and return the resulting measurement probability distribution.

    This function tests a state-preparation circuit by measuring all qubits 
    and returning the counts of each computational basis state over a specified 
    number of shots.

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to be tested.
    shots : int
        Number of measurement repetitions to estimate probabilities.

    Returns
    -------
    dict
        A dictionary mapping computational basis states (as integers) to 
        the number of times each state was measured.

    Example
    -------
    >>> qc = QuantumCircuit(2)
    >>> qc.h(0)
    >>> counts = circuit_test(qc, shots=1024)
    >>> print(counts)
    {0: 512, 1: 512, ...}
    """
    n = qc.num_qubits

    # Create a full circuit with classical registers for measurement
    qc_test = QuantumCircuit(n, n)
    qc_test.append(qc, qc_test.qubits[:]) # type: ignore
    qc_test.measure(qc_test.qubits[:], qc_test.clbits[:])

    # Execute the circuit and get measurement results
    count_dict = circuit_execution(qc_test, shots)

    return count_dict

def bit_controlled_preparation_2MS(n: int, m: int, qc: QuantumCircuit) -> QuantumCircuit:
    """
    Prepare a mixed quantum state controlled by classical measurement bits.

    This function constructs two possible mixed states based on the outcomes 
    of classical control bits. Given `n` target qubits, the two states are:

    .. math::
        ρ₁ = 1 / (2^(n-1)) * (|0⟩⟨0| + ... + |2^(n-1)-1⟩⟨2^(n-1)-1|)

        ρ₂ = 1 / (2^(n-1)) * (|2^(n-1)⟩⟨2^(n-1)| + ... + |2^n-1⟩⟨2^n-1|)

    Example for n = 2:
        ρ₁ = 1/2 * (|0⟩⟨0| + |1⟩⟨1|)
        ρ₂ = 1/2 * (|2⟩⟨2| + |3⟩⟨3|)

    Parameters
    ----------
    n : int
        Number of target qubits used to construct the mixed state.
    m : int
        Number of control qubits whose measurement outcomes determine 
        which state is prepared.
    qc : QuantumCircuit
        The quantum circuit to which the controlled mixed-state preparation 
        will be applied.

    Returns
    -------
    QuantumCircuit
        The input circuit with the additional operations implementing 
        bit-controlled mixed-state preparation.

    Example
    -------
    >>> from qiskit import QuantumCircuit
    >>> qc = QuantumCircuit(5, 5)  # n=2 target qubits, m=3 control qubits
    >>> qc = bit_controlled_preparation_2MS(n=2, m=3, qc=qc)
    >>> print(qc)

    Example circuit (n=2, m=3)::

                 ┌─┐
            q_0: ┤M├───────────
                 └╥┘
            q_1: ─╫────────────
                  ║
            q_2: ─╫────────────
                  ║    ┌───┐
            q_3: ─╫────┤ X ├───
                  ║    └─╥─┘
            q_4: ─╫──────╫─────
                  ║ ┌────╨────┐
            c: 5/═╩═╡ c_4=0x1 ╞
                  4 └─────────┘
    
    """
    for index in range(m, n + m - 1):
        qc.measure(qc.qubits[index - m], qc.clbits[-1])
        qc.x(qc.qubits[index]).c_if(qc.clbits[-1], 1)
    return qc

def qubit_controlled_preparation_2MS(n: int, m: int, qc: QuantumCircuit) -> QuantumCircuit:
    """
    Prepare a mixed quantum state controlled directly by qubits.

    This function constructs two possible mixed states using qubit-controlled 
    operations. Given `n` target qubits, the two states are:

    .. math::
        ρ₁ = 1 / (2^(n-1)) * (|0⟩⟨0| + ... + |2^(n-1)-1⟩⟨2^(n-1)-1|)

        ρ₂ = 1 / (2^(n-1)) * (|2^(n-1)⟩⟨2^(n-1)| + ... + |2^n-1⟩⟨2^n-1|)

    Example for n = 2:
        ρ₁ = 1/2 * (|0⟩⟨0| + |1⟩⟨1|)
        ρ₂ = 1/2 * (|2⟩⟨2| + |3⟩⟨3|)

    Parameters
    ----------
    n : int
        Number of target qubits used to construct the mixed state.
    m : int
        Number of control qubits whose quantum state directly controls 
        the preparation.
    qc : QuantumCircuit
        The quantum circuit to which the qubit-controlled mixed-state 
        preparation will be applied.

    Returns
    -------
    QuantumCircuit
        The input circuit with the additional operations implementing 
        qubit-controlled mixed-state preparation.

    Example
    -------
    >>> from qiskit import QuantumCircuit
    >>> qc = QuantumCircuit(5, 5)  # n=2 target qubits, m=3 control qubits
    >>> qc = qubit_controlled_preparation_2MS(n=2, m=3, qc=qc)
    >>> print(qc)

    Example circuit (n=2, m=3)::

                      ┌─┐   
            q_0: ──■──┤M├───
                   │  └╥┘┌─┐
            q_1: ──┼───╫─┤M├
                   │   ║ └╥┘
            q_2: ──┼───╫──╫─
                 ┌─┴─┐ ║  ║ 
            q_3: ┤ X ├─╫──╫─
                 └───┘ ║  ║
            q_4: ──────╫──╫─
                       ║  ║
            c: 5/══════╩══╩═
                       4  4
    
    """
    for index in range(m, n + m - 1):
        qc.cx(qc.qubits[index - m], qc.qubits[index])
    for i in range(n):
        qc.measure(qc.qubits[i], qc.clbits[-1])
    return qc

def bit_controlled_preparation_1MS(n: int, m: int, qc: QuantumCircuit) -> QuantumCircuit:
    """
    Prepare a single mixed quantum state controlled by classical measurement bits.

    This function covers a set of classical inputs with one mixed state. 
    For example, when `n = 2` target qubits:

    .. math::
        ρ = 1/4 * (|0⟩⟨0| + |1⟩⟨1| + |2⟩⟨2| + |3⟩⟨3|)

    Parameters
    ----------
    n : int
        Number of target qubits used to construct the mixed state.
    m : int
        Number of control qubits whose measurement outcomes determine 
        which operations are applied.
    qc : QuantumCircuit
        The quantum circuit to which the bit-controlled mixed-state 
        preparation will be applied.

    Returns
    -------
    QuantumCircuit
        The input circuit with the additional operations implementing 
        bit-controlled single mixed-state preparation.

    Example
    -------
    >>> from qiskit import QuantumCircuit
    >>> qc = QuantumCircuit(5, 5)  # n=2 target qubits, m=3 control qubits
    >>> qc = bit_controlled_preparation_1MS(n=2, m=3, qc=qc)
    >>> print(qc)

    Example circuit (n=2, m=3)::

                 ┌─┐
            q_0: ┤M├─────────────────────────
                 └╥┘           ┌─┐
            q_1: ─╫────────────┤M├───────────
                  ║            └╥┘
            q_2: ─╫─────────────╫────────────
                  ║    ┌───┐    ║
            q_3: ─╫────┤ X ├────╫────────────
                  ║    └─╥─┘    ║    ┌───┐
            q_4: ─╫──────╫──────╫────┤ X ├───
                  ║      ║      ║    └─╥─┘
                  ║ ┌────╨────┐ ║ ┌────╨────┐
            c: 5/═╩═╡ c_4=0x1 ╞═╩═╡ c_4=0x1 ╞
                  4 └─────────┘ 4 └─────────┘
    
    """
    for index in range(m, n + m):
        qc.measure(qc.qubits[index - m], qc.clbits[-1])
        qc.x(qc.qubits[index]).c_if(qc.clbits[-1], 1)
    return qc

def qubit_controlled_preparation_1MS(n: int, m: int, qc: QuantumCircuit) -> QuantumCircuit:
    """
    Prepare a mixed state controlled by qubits.

    This routine covers a group of classical inputs using a single mixed state.
    For example, when ``n = 2``, the resulting density matrix is::

        ρ = 1/4 * (|0⟩⟨0| + |1⟩⟨1| + |2⟩⟨2| + |3⟩⟨3|)

    The mixed state is generated by applying controlled operations from the
    control qubits to the target qubits.

    Parameters
    ----------
    n : int
        Number of target qubits.
    m : int
        Number of control qubits.
    qc : QuantumCircuit
        Quantum circuit where the control state preparation has already been
        defined.

    Returns
    -------
    QuantumCircuit
        The quantum circuit updated with mixed state preparation.

    Example
    -------
    >>> n, m = 2, 3
    >>> qc = QuantumCircuit(n + m, n + m)
    >>> qc = qubit_controlled_preparation_1MS(n, m, qc)
    >>> print(qc)

    Example circuit (n=2, m=3)::

                           ┌─┐   
            q_0: ──■───────┤M├───
                   │       └╥┘┌─┐
            q_1: ──┼────■───╫─┤M├
                   │    │   ║ └╥┘
            q_2: ──┼────┼───╫──╫─
                 ┌─┴─┐  │   ║  ║
            q_3: ┤ X ├──┼───╫──╫─
                 └───┘┌─┴─┐ ║  ║
            q_4: ─────┤ X ├─╫──╫─
                      └───┘ ║  ║
            c: 5/═══════════╩══╩═
                            4  4
    
    """
    for index in range(m, n + m):
        qc.cx(qc.qubits[index - m], qc.qubits[index])
    for i in range(n):
        qc.measure(qc.qubits[i], qc.clbits[-1])
    return qc  

# Remember its necessary to record the measurement results of control qubits
def bit_controlled_preparation_MPS(n, m, qc):
    """
    Prepare a mixed state controlled by classical bits.

    This routine prepares a hybrid state consisting of:
    
    - A mixed state that spans computational basis states 
      ``|0⟩⟨0|`` through ``|2^n-2⟩⟨2^n-2|``.
    - A pure state corresponding to ``|2^n-1⟩⟨2^n-1|``.

    This construction is particularly useful for testing 
    *repeat-until-success* structures when the number of 
    target states ``N`` is not a power of ``m``.

    For example, when ``n = 2``::

        ρ₁ = 1/3 * (|0⟩⟨0| + |1⟩⟨1| + |2⟩⟨2|)
        ρ₂ = |3⟩⟨3|

    Parameters
    ----------
    n : int
        Number of target qubits.
    m : int
        Number of control qubits.
    qc : QuantumCircuit
        Quantum circuit where control state preparation 
        has already been defined.

    Returns
    -------
    QuantumCircuit
        The quantum circuit updated with mixed state preparation.

    Example
    -------
    >>> n, m = 2, 3
    >>> qc = QuantumCircuit(n + m, n + m)
    >>> qc = bit_controlled_preparation_MPS(n, m, qc)
    >>> print(qc)

    Example circuit (n=2, m=3)::

                 ┌─┐
            q_0: ┤M├─────────────────────────
                 └╥┘┌─┐
            q_1: ─╫─┤M├──────────────────────
                  ║ └╥┘
            q_2: ─╫──╫───────────────────────
                  ║  ║    ┌───┐
            q_3: ─╫──╫────┤ X ├──────────────
                  ║  ║    └─╥─┘      ┌───┐
            q_4: ─╫──╫──────╫────────┤ X ├───
                  ║  ║      ║        └─╥─┘
                  ║  ║ ┌────╨────┐┌────╨────┐
            c: 5/═╩══╩═╡ c_0=0x1 ╞╡ c_1=0x1 ╞
                  0  1 └─────────┘└─────────┘            
    
    """
    for index in range(m, n + m):
        qc.measure(qc.qubits[index - m], qc.clbits[index - m])
        qc.x(qc.qubits[index]).c_if(qc.clbits[index - m], 1)
    return qc

def qubit_controlled_preparation_MPS(n: int, m: int, qc: QuantumCircuit) -> QuantumCircuit:
    """
    Prepare a hybrid mixed-and-pure state controlled by qubits.

    This function prepares a system consisting of:
    
    - A mixed state spanning the computational basis states |0⟩⟨0| through |2^n-2⟩⟨2^n-2|, and
    - A pure state corresponding to |2^n-1⟩⟨2^n-1|.

    This is particularly useful for testing *repeat-until-success* 
    structures when the total number of target states is not a power of the number of control qubits.

    For example, when `n = 2`::

        ρ₁ = 1/3 * (|0⟩⟨0| + |1⟩⟨1| + |2⟩⟨2|)
        ρ₂ = |3⟩⟨3|

    Parameters
    ----------
    n : int
        Number of target qubits.
    m : int
        Number of control qubits.
    qc : QuantumCircuit
        Quantum circuit where the control qubits are already prepared.

    Returns
    -------
    QuantumCircuit
        The quantum circuit updated with the hybrid mixed-pure state preparation.

    Example
    -------
    >>> n, m = 2, 3
    >>> qc = QuantumCircuit(n + m, n + m)
    >>> qc = qubit_controlled_preparation_MPS(n, m, qc)
    >>> print(qc)

    Example circuit (n=2, m=3)::

                              ┌─┐
            q_0: ──■──────────┤M├───
                   │          └╥┘┌─┐
            q_1: ──┼────■──────╫─┤M├
                   │    │  ┌─┐ ║ └╥┘
            q_2: ──┼────┼──┤M├─╫──╫─
                 ┌─┴─┐  │  └╥┘ ║  ║
            q_3: ┤ X ├──┼───╫──╫──╫─
                 └───┘┌─┴─┐ ║  ║  ║
            q_4: ─────┤ X ├─╫──╫──╫─
                      └───┘ ║  ║  ║
            c: 5/═══════════╩══╩══╩═
                            2  0  1
    """
    # Apply controlled-NOT gates from control qubits to target qubits
    for index in range(m, n + m):
        qc.cx(qc.qubits[index - m], qc.qubits[index])

    # Measure control qubits
    for i in range(m):
        qc.measure(qc.qubits[i], qc.clbits[i])

    return qc

if __name__ == "__main__":
    """
    Manual check for all preparation circuits.
    Run:
        python -m mycode.utils.preparation_circuits
    """

    shots = 1024  # For consistency; not used in manual checks

    # ----------------------------
    # Test inputs
    # ----------------------------

    def test_input_separable_circuit():  
        return [math.pi/3, math.pi/2, math.pi/4]

    def test_input_entangled_circuit():
        return [2*math.pi/3, math.pi/6, math.pi/3]

    def test_input_mixed_states():
        n, m = 2, 2
        qc = QuantumCircuit(n+m, n+m)
        return qc, n, m

    # ----------------------------
    # Manual check functions
    # ----------------------------

    def manual_check_separable_circuit(theta_list, shots):
        qc = separable_control_state_preparation(theta_list)
        print("\n--- Separable Control Circuit ---")
        print(qc.draw(output='text'))

    def manual_check_entangled_circuit(theta_list, shots):
        qc = entangled_control_state_preparation(theta_list)
        print("\n--- Entangled Control Circuit ---")
        print(qc.draw(output='text'))

    def manual_check_bit_controlled_1MS(qc_n_m_tuple, shots):
        qc, n, m = qc_n_m_tuple
        qc_new = bit_controlled_preparation_1MS(n, m, qc)
        print("\n--- Bit-Controlled 1MS Circuit ---")
        print(qc_new.draw(output='text'))

    def manual_check_qubit_controlled_1MS(qc_n_m_tuple, shots):
        qc, n, m = qc_n_m_tuple
        qc_new = qubit_controlled_preparation_1MS(n, m, qc)
        print("\n--- Qubit-Controlled 1MS Circuit ---")
        print(qc_new.draw(output='text'))

    def manual_check_bit_controlled_2MS(qc_n_m_tuple, shots):
        qc, n, m = qc_n_m_tuple
        qc_new = bit_controlled_preparation_2MS(n, m, qc)
        print("\n--- Bit-Controlled 2MS Circuit ---")
        print(qc_new.draw(output='text'))

    def manual_check_qubit_controlled_2MS(qc_n_m_tuple, shots):
        qc, n, m = qc_n_m_tuple
        qc_new = qubit_controlled_preparation_2MS(n, m, qc)
        print("\n--- Qubit-Controlled 2MS Circuit ---")
        print(qc_new.draw(output='text'))

    def manual_check_bit_controlled_MPS(qc_n_m_tuple, shots):
        qc, n, m = qc_n_m_tuple
        qc_new = bit_controlled_preparation_MPS(n, m, qc)
        print("\n--- Bit-Controlled MPS Circuit ---")
        print(qc_new.draw(output='text'))

    def manual_check_qubit_controlled_MPS(qc_n_m_tuple, shots):
        qc, n, m = qc_n_m_tuple
        qc_new = qubit_controlled_preparation_MPS(n, m, qc)
        print("\n--- Qubit-Controlled MPS Circuit ---")
        print(qc_new.draw(output='text'))

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {"input": test_input_separable_circuit, "shots": shots, "function": manual_check_separable_circuit},
        "1": {"input": test_input_entangled_circuit, "shots": shots, "function": manual_check_entangled_circuit},
        "2": {"input": test_input_mixed_states, "shots": shots, "function": manual_check_bit_controlled_1MS},
        "3": {"input": test_input_mixed_states, "shots": shots, "function": manual_check_qubit_controlled_1MS},
        "4": {"input": test_input_mixed_states, "shots": shots, "function": manual_check_bit_controlled_2MS},
        "5": {"input": test_input_mixed_states, "shots": shots, "function": manual_check_qubit_controlled_2MS},
        "6": {"input": test_input_mixed_states, "shots": shots, "function": manual_check_bit_controlled_MPS},
        "7": {"input": test_input_mixed_states, "shots": shots, "function": manual_check_qubit_controlled_MPS},
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