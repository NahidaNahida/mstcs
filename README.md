# mstcs
This repository includes the all code and data involved in the paper "*Preparation and Utilization of Mixed States for Testing Quantum Programs*" that has been accepted as a journal-first paper at ACM Transactions on Software Engineering and Methodology (TOSEM).

MSTCs (i.e., mixed-state test cases) is a new concept proposed in our paper. It suggests preparing and utilizing mixed states as the test inputs for quantum programs, since the mixed states have the power to represent multiple pure states in a probabilistic manner. The empirical evaluation of MSTCs is based on the quantum software development kits Qiskit, and the backend is selected as an ideal simulator. For more details, please refer to our paper.

## Release Notes

### Prelude

+ v1: The code was updated due to the major revision of a submitted manuscript (released at 2025-03-06).
+ v2: This repository was refactored and updated for better replicability, where the raw experimental results reported in the paper are provided as well. (released at 2025-05-16).

### Reported changes 

#### v1

+ Add a new folder `Linear Amplitude Function` corresponding to the newly introduced object program.
+ Add `xxx_defect6.py` for each object program folder, because of a newly included buggy version.
+ `xxx_RQ1.py` is updated to record the time for state preparation.
+ The maximum of classical inputs $n$ in `xxx_RQ1.py` and `xxx_RQ3.py` increase to 6.
+ `xxx_versions_info.md` adds the description for complexity that is derived from the corresponding `xxx_circuit_info.py`.
+ Part of the codes are slightly reconstructed.

`xxx` is denoted as one of `Id`, `comp`, `pauli`, `amplitude`, `quad`, `qft` and `adder`.

#### v2

+ Refactor some code in the previous repository.
+ All the previous files for implementation are in the folder `code`.
+ The two notebooks, `drawing_figures.ipynb` and `motivational_example.ipynb`, are added for data analysis and virtualization.
+ The raw data and figures corresponding to empirical studies are included in the folder `data`.

## Requirements

```
numpy==2.1.2
qiskit==0.46.2
qiskit_aer==0.13.3
qiskit_terra==0.46.2
scipy==1.14.1
```

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
