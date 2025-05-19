# mstcs 
MSTCs (i.e., mixed-state test cases) is a new concept proposed in our paper. It suggests preparing and utilizing mixed states as the test inputs for quantum programs, since the mixed states have the power to represent multiple pure states in a probabilistic combination. Therefore, an MSTC demonstrates a higher input domain coverage than a PSTC (i.e., pure-state test cases) that are widely discussed in existing works, thereby contributing to the test effectiveness and efficiency. The empirical evaluation of MSTCs is based on the quantum software development kits Qiskit, and the backend is selected as an ideal simulator. For more details, please refer to our paper.

## Publication

This repository includes the all code and data involved in the paper "*Preparation and Utilization of Mixed States for Testing Quantum Programs*" that has been accepted as a journal-first paper at ACM Transactions on Software Engineering and Methodology (TOSEM).

## Steps for Replication

### Getting Started

1. Use the following commend line to clone this repository.

   ```
   git clone https://github.com/NahidaNahida/mstcs.git
   ```

2. Set up the environment instructed by [INSTALL.md](https://github.com/NahidaNahida/mstcs/blob/main/INSTALL.md).

Note: We also provide an available [docker image](https://github.com/NahidaNahida/mstcs/pkgs/container/mstcs-container) with Linux/amd64, which will contain all you need to run this artifact.

### Running for RQs

We offer a running example to replicate the empirical results for involved object programs and research questions. First, change the directory to `code` (via `cd code`) and run the following commend

```
python run.py PROGRAM RQ
```

where, 

+ `PROGRAM`:  The full name of object program (i.e., `Identity`, `IntegerComparator`, `LinearAmplitudeFunction`, `LinearPauliRotations`, `QuadraticForm`, `QuantumFourierTransform`, and `WeightedAdder`).
+ `RQ`: The name of the research question (i.e., `RQ1`, `RQ2`, `RQ3`, `RQ4`, `RQ5`, and `RQ6`).

The yielded results (stored as a `.csv` file) are saved to `./data/raw_data_for_empirical_results/RQ/PROGRAM` automatically.

### Data Analysis




## Documentation of Components

## Folders for testing the object programs

There are 7 folders (i.e., `Identity`, `Integer Comparator`, `Linear Pauli Rotations`, `Linear Amplitude Function`, `Quadratic Form`, `Quantum Fourier Transform` and `Weighted Adder`) that correspond to the object programs used in the manuscript. These 6 real-world quantum programs (except `Identity` of the above 7) can be found at `qiskit.circuit.library` (https://github.com/Qiskit/qiskit/tree/stable/1.2/qiskit/circuit/library).

For each folder, the following types of files are included.

+ `xxx.py`:

  The raw version of each quantum program.

+ `xxx_circuit_info.py`:

  This file is used to collect basic information (# Qubits, # Gates and #Depths) of the quantum circuit corresponding to each program version. The relevant results are displayed in Table 3 of the manuscript.

+ `xxx_specification.py`:

  This file calculates the expected output distribution according to the formula-based program specification provided by Qiskit. The functions `PSTC_specification` and `MSTC_specification` respectively correspond to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).

+ `xxx_versions_info.md`:

  This file details the manually implanted bugs mentioned in Table 3 of the manuscript.

+ `xxx_defecti.py`:

  The buggy version mutated from the raw one. `i` indicates the name of the buggy version. For example, `adder_defect2.py` is the `v2` of the object `WA`.

+ `xxx_RQj.py`:

  This file implements the experiment for RQ`j`, where `j`=1, 2, 3, 4, 5 and 6. **When replicating the experiment, please run this file directly**.

## Files of involved functions

+ `data_convertion.py`:

  This file is used for preprocessing of data.

  + `generate_numbers(n, m)`:  Generate all the n-digit m-ary numbers and store them at corresponding lists.
  + `output_prob(counts, n)`: The list of measurement results is transformed into corresponding probability.

+ `preparation_circuits.py`: 

  This file includes several functions related to the quantum circuits for the preparation of control states and the controlled preparation of mixed states. These functions are mainly used for the experiments of RQ2 and RQ4. For more details, please refer to this file.

+ `circuit_execution.py`:

  This file aims to execute the quantum circuit. Upon the backend `qsam_simulator`, the dictionary of the measurement results can be yielded.

+ `repeat_until_success.py`:

  It is used to achieve the repeat-until-success (RUS) structure using Qiskit. The RUS structure is discussed in Section 5.2.1(Separable Control States) of the manuscript.

+ `test_oracle.py`:

  The test oracle is included in this file. More particularly, output probability oracle (OPO) is employed for MSTCs, and the Mann-Whitney U test compares two sample groups.
