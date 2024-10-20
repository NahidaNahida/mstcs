import random
from circuit_execution import circuit_execution

def repeat_until_success(qc, shots, invalid_list):
    '''
        Given a quantum circuit, repeat executing it until no more invalid outputs.
        This function can be used to produce a result that follows U(0, 2) with n=2.
        
        Input variables:
            + qc:           the quantum circuit
            + shots:        the number of shots
            + invalid_list  the list of numbers that are not expected to be yielded
        
        Output variable:
            + final_counts  the dictionary of the measurement results

        Running example:
            Run the following codes, where we hope the results of control qubits follows the
            uniform distribution and ranges in {0, 1, 2}.

                qc = QuantumCircuit(3, 3)
                m = 2
                qc.h(qc.qubits[:2])
                qc.measure(qc.qubits[:], qc.clbits[:])
                final_counts = repeat_until_success(qc, 1000, [3])
                print(final_counts)

            The output is 

                {1: 307, 2: 357, 0: 336}
    '''
    flag = 0
    while True:
        dict_counts = circuit_execution(qc, shots)
        temp_dict_counts = dict_counts.copy()
        # remove invalid control instruction
        keys_to_remove = [key for key in temp_dict_counts if key in invalid_list]
        for key in keys_to_remove:
            del temp_dict_counts[key]
        if flag == 0:             # the first run
            flag = 1
            final_counts = temp_dict_counts.copy()
        else:
            # randomly selecting (remained_samps) samples                
            samps_list = list(temp_dict_counts.keys())
            counts_list = list(temp_dict_counts.values())
            sel_samps = random.choices(samps_list, weights=counts_list, k=remained_samps)
            sampled_dict = {}
            # save to new dictionary
            for sample in sel_samps:
                if sample in sampled_dict:
                    sampled_dict[sample] += 1
                else:
                    sampled_dict[sample] = 1
            # merge the dictionary
            for key, value in sampled_dict.items():
                if key in dict_counts:
                    final_counts[key] += value
                else:
                    final_counts[key] = value
        # check the number of valid samples
        temp_samps = sum(final_counts.values())
        remained_samps = shots - temp_samps
        if remained_samps == 0:
            return final_counts

def generate_invalid_numbers(total_bits, con_bits, invalid_con_list):
    '''
        When the decimal values of invalid control qubits are given and all the qubits (i.e., control
        and target ones) are measured, generate all the possible decimal values of invalid measurement 
        results.

        Input variables:
            + total_bits        the number of all the involved qubits
            + con_bits          the number of control qubits
            + invalid_con_list  the list of invalid values of control qubits (decimal)

        Output variable:
            + invalid_num_list  the list of invalid values of measurement results (decimal)

        Running example:
            Run the following codes

                n = 2
                m = 3
                invalid_con_list = [6, 7]
                invalid_num_list = generate_invalid_numbers(n + m, m, invalid_con_list)
                print(invalid_num_list)

            The displayed output should be
            
                [6, 7, 14, 15, 22, 23, 30, 31]
            
            where the low m=3 bits are 110 (decimal 6) and 111 (decimal 7).
    '''
    # calculate the number of target qubits, where the control bits are default as low ones.
    high_bits = total_bits - con_bits
    invalid_num_list = []
    for high in range(2**high_bits):
        for invalid_con in invalid_con_list:
            combined_binary = (high << con_bits) | invalid_con
            invalid_num_list.append(combined_binary)
    return invalid_num_list