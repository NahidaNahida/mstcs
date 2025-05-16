import math
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import RYGate 
from qiskit import QuantumCircuit
import numpy as np
from circuit_execution import circuit_execution

def separable_control_state_preparation(theta_list):
    '''
        Prepare separable control states according to the given thetas.

        Input variable:
            + theta_list: [list]            m thetas for the rotation gates
        
        Output variable:
            + qc:         [QuantumCircuit]  the quantum circuit for preparing the separable state
        
        Running example：
            Use the following inputs:
                theta_list = [math.pi / 2, math.pi / 2]
            The corresponding quantum circuit turns out to be
                     ┌─────────┐
                q_0: ┤ Ry(π/2) ├
                     ├─────────┤
                q_1: ┤ Ry(π/2) ├
                     └─────────┘
    '''
    m = len(theta_list)
    qc = QuantumCircuit(m)
    for index, theta in enumerate(theta_list):
        qc.ry(theta, index)
    return qc

def separable_control_state_probs(theta_list):
    '''
        Return the probability distributions corresponding to separable preparation of control states.

        Input variable:
            + theta_list:   [list]  m thetas for the rotation gates
        
        Output variable:
            + output_probs: [list]  the list of output probability distribution
    '''
    for index, theta in enumerate(theta_list):
        temp_state = np.array([math.cos(theta/2), math.sin(theta/2)])
        if index == 0:
            final_state = temp_state
        else:
            final_state = np.kron(temp_state, final_state)
    output_probs = final_state ** 2
    return output_probs.tolist() 

def entangled_control_state_preparation(theta_list):
    '''
        Prepare entangled control states according to the given thetas.

        Input variable:
            + theta_list: [list]            (2^m-1) thetas for the rotation gates
        
        Output variable:
            + qc:         [QuantumCircuit]  the quantum circuit for preparing the separable state

        Running example：
            Use the following inputs:
                theta_list = [2 * math.pi / 3, math.pi / 6, math.pi / 3]
            The corresponding quantum circuit turns out to be
                     ┌──────────┐┌───┐           ┌───┐
                q_0: ┤ Ry(2π/3) ├┤ X ├─────■─────┤ X ├─────■─────
                     └──────────┘└───┘┌────┴────┐└───┘┌────┴────┐
                q_1: ─────────────────┤ Ry(π/6) ├─────┤ Ry(π/3) ├
                                      └─────────┘     └─────────┘
    '''

    def processed_qubits(decimal_num, bits):
        # transform decimal number to binary string
        binary_str = bin(decimal_num)[2:].zfill(bits)
        # yield which bit refers to 0                                                 
        positions_of_ones = [i for i, digit in enumerate(binary_str[::-1]) if digit == '0'] 
        return positions_of_ones

    m = int(math.log2(len(theta_list) + 1))
    qc = QuantumCircuit(m)

    for i in range(m):
        if i == 0:                          
            qc.ry(theta_list[0], 0)
            theta_index = 1
        else:
            qubit_index_i = [k for k in range(i + 1)]               
            for j in range(0, int(math.pow(2, i)), 1):                                 
                qubit_index_j = processed_qubits(j, i)
                if len(qubit_index_j) > 0:
                    # apply within-apply structure
                    qc.x(qubit_index_j)
                    qc.append(RYGate(theta_list[theta_index]).control(i), qubit_index_i)
                    qc.x(qubit_index_j)
                else:
                    qc.append(RYGate(theta_list[theta_index]).control(i), qubit_index_i)
                theta_index = theta_index + 1
    return qc  

def circuit_test(qc, shots):
    '''
        Check the probability distribution produced from the state preparation
        
        Input variables:
            + qc:        [QuantumCircuit]   the quantum circuit to be tested
            + shots:     [int]              the number of shots
        
        Output variable:
            + count_dict [dict]             the dictionary of the measurement results
    '''
    n = qc.num_qubits
    qc_test = QuantumCircuit(n, n)
    qc_test.append(qc, qc_test.qubits[:])
    qc_test.measure(qc_test.qubits[:], qc_test.clbits[:])
    count_dict = circuit_execution(qc_test, shots)
    return count_dict

def bit_controlled_preparation_2MS(n, m, qc):
    """
        The preparation of the mixed state is controlled by bits.

        Cover a group of classical inputs with two mixed state. Given n,
            rho1 = 1/(2^(n-1)) * (|0><0| + ... + |2^{n-1}-1><2^{n-1}-1|) 
            rho2 = 1/(2^(n-1)) * (|2^{n-1}><2^{n-1}| + ... + |2^{n}-1><2^{n}-1|).
        
        For example, n = 2,
        rho1 = 1/2 * (|0><0| + |1><1|) 
        rho2 = 1/2 * (|2><2| + |3><3|)

        Input variable: 
            + n:    [int]               the number of target qubits
            + m:    [int]               the number of control qubits
            + qc:   [QuantumCircuit]    the quantum circuit for preparing control states
        Output variable:
            + qc:   [QuantumCircuit]    the quantum circuit for the mixed state preparation
        
        Running example:
            n = 2, m = 3, qc = QuantumCircuit(n + m, n + m)
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

def qubit_controlled_preparation_2MS(n, m, qc):
    """
        The preparation of the mixed state is controlled by quits.

        Cover a group of classical inputs with two mixed state. Given n,
            rho1 = 1/(2^(n-1)) * (|0><0| + ... + |2^{n-1}-1><2^{n-1}-1|) 
            rho2 = 1/(2^(n-1)) * (|2^{n-1}><2^{n-1}| + ... + |2^{n}-1><2^{n}-1|).
        
        For example, n = 2,
        rho1 = 1/2 * (|0><0| + |1><1|) 
        rho2 = 1/2 * (|2><2| + |3><3|)

        Input variable: 
            + n:    [int]               the number of target qubits
            + m:    [int]               the number of control qubits
            + qc:   [QuantumCircuit]    the quantum circuit for preparing control states
        Output variable:
            + qc:   [QuantumCircuit]    the quantum circuit for the mixed state preparation
        
        Running example:
        n = 2, m = 3, qc = QuantumCircuit(n + m, n + m)
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

def bit_controlled_preparation_1MS(n, m, qc):
    """
        The preparation of the mixed state is controlled by bits.

        Cover a group of classical inputs with only one mixed state. For example, n = 2,
        rho = 1/4 * (|0><0| + |1><1| + |2><2| + |3><3|)

        Input variable: 
            + n:    [int]               the number of target qubits
            + m:    [int]               the number of control qubits
            + qc:   [QuantumCircuit]    the quantum circuit for preparing control states
        Output variable:
            + qc:   [QuantumCircuit]    the quantum circuit for the mixed state preparation
        
        Running example:
        n = 2, m = 3, qc = QuantumCircuit(n + m, n + m)
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

def qubit_controlled_preparation_1MS(n, m, qc):
    """
        The preparation of the mixed state is controlled by quits.

        Cover a group of classical inputs with only one mixed state. For example, n = 2,
        rho = 1/4 * (|0><0| + |1><1| + |2><2| + |3><3|)

        Input variable: 
            + n:    [int]               the number of target qubits
            + m:    [int]               the number of control qubits
            + qc:   [QuantumCircuit]    the quantum circuit for preparing control states
        Output variable:
            + qc:   [QuantumCircuit]    the quantum circuit for the mixed state preparation
        
        Running example:
        n = 2, m = 3, qc = QuantumCircuit(n + m, n + m)
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

# remember its necessary to record the measurement results of control qubits
def bit_controlled_preparation_MPS(n, m, qc):
    """
        The preparation of the mixed state is controlled by bits.
        
        Cover a group of classical inputs with one mixed state and one pure state. 
        The mixed state includes |0><0| ~ |2^n-2><2^n-2| and the pure states is |2^n-1><2^n-1|.
        Especially, this aims to check the repeat-until-success structure when N is not a power of m
        For example, n = 2,
        rho1 = 1/3 * (|0><0| + |1><1| + |2><2|), rho2 = |3><3|

        Input variable: 
            + n:    [int]               the number of target qubits
            + m:    [int]               the number of control qubits
            + qc:   [QuantumCircuit]    the quantum circuit for preparing control states
        Output variable:
            + qc:   [QuantumCircuit]    the quantum circuit for the mixed state preparation

        Running example:
            n = 2, m = 3, qc = QuantumCircuit(n + m, n + m)
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

def qubit_controlled_preparation_MPS(n, m, qc):
    """
        The preparation of the mixed state is controlled by bits.
        
        Cover a group of classical inputs with one mixed state and one pure state. 
        The mixed state includes |0><0| ~ |2^n-2><2^n-2| and the pure states is |2^n-1><2^n-1|.
        Especially, this aims to check the repeat-until-success structure when N is not a power of m
        For example, n = 2,
        rho1 = 1/3 * (|0><0| + |1><1| + |2><2|), rho2 = |3><3|

        Input variable: 
            + n:    [int]               the number of target qubits
            + m:    [int]               the number of control qubits
            + qc:   [QuantumCircuit]    the quantum circuit for preparing control states
        Output variable:
            + qc:   [QuantumCircuit]    the quantum circuit for the mixed state preparation

        Running example:
            n = 2, m = 3, qc = QuantumCircuit(n + m, n + m)
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
    for index in range(m, n + m):
        qc.cx(qc.qubits[index - m], qc.qubits[index])
    for i in range(m):
        qc.measure(qc.qubits[i], qc.clbits[i])
    return qc