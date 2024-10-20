# Preparation-and-Utilization-of-Mixed-States-for-Testing-Quantum-Programs
This project includes the code and data involved in the manuscript '*Preparation and Utilization of Mixed States for Testing Quantum Programs*'. 

The tree structure of this project is shown as follows.

```
│  circuit_execution.py
│  data_convertion.py
│  preparation_circuits.py
│  readme.md
│  repeat_until_success.py
│  requirements.txt
│  test_oracle.py
│
├─Identity
│      id_RQ1.py
│      id_RQ2.py
│      id_specification.py
│
├─Integer Comparator
│      comp.py
│      comp_defect.py
│      comp_defect1.py
│      comp_defect2.py
│      comp_defect3.py
│      comp_defect4.py
│      comp_defect5.py
│      comp_info.py
│      comp_RQ1.py
│      comp_RQ2.py
│      comp_RQ3.py
│      comp_RQ4.py
│      comp_RQ5.py
│      comp_specification.py
│      comp_versions_info.md
│
├─Linear Pauli Rotations
│      linear.py
│      linear_circuit_info.py
│      linear_defect1.py
│      linear_defect2.py
│      linear_defect3.py
│      linear_defect4.py
│      linear_defect5.py
│      linear_RQ1.py
│      linear_RQ2.py
│      linear_RQ3.py
│      linear_RQ4.py
│      linear_RQ5.py
│      linear_specification.py
│      linear_versions_info.md
│
├─Quadratic Form
│      quad.py
│      quad_circuit_info.py
│      quad_defect1.py
│      quad_defect2.py
│      quad_defect3.py
│      quad_defect4.py
│      quad_defect5.py
│      quad_RQ1.py
│      quad_RQ2.py
│      quad_RQ3.py
│      quad_RQ4.py
│      quad_RQ5.py
│      quad_specification.py
│      quad_versions_info.md
│
├─Quantum Fourier Transform
│      qft.py
│      qft_circuit_info.py
│      qft_defect1.py
│      qft_defect2.py
│      qft_defect3.py
│      qft_defect4.py
│      qft_defect5.py
│      qft_RQ1.py
│      qft_RQ2.py
│      qft_RQ3.py
│      qft_RQ4.py
│      qft_RQ5.py
│      qft_specification.py
│      qft_versions_info.md
│
└─Weighted Adder
        adder.py
        adder_circuit_info.py
        adder_defect1.py
        adder_defect2.py
        adder_defect3.py
        adder_defect4.py
        adder_defect5.py
        adder_RQ1.py
        adder_RQ2.py
        adder_RQ3.py
        adder_RQ4.py
        adder_RQ5.py
        adder_specification.py
        adder_versions_info.md
```

    ​The author welcomes replicability works and further studies based on this project. Should there be any technical and academic questions, please do not hesitate to contact the author (liyuechen@buaa.edu.cn).

## Requirements

```
numpy==2.1.2
qiskit==0.46.2
qiskit_aer==0.13.3
qiskit_terra==0.46.2
scipy==1.14.1
```

## Folders for testing the object programs

    ​There are 6 folders (i.e., `Identity`, `Integer Comparator`, `Linear Pauli Rotations`, `Quadratic Form`, `Quantum Fourier Transform` and `Weighted Adder`) that correspond to the object programs used in the manuscript. These 5 real-world quantum programs (except `Identity` of the six) can be found at `qiskit.circuit.library` (https://github.com/Qiskit/qiskit/tree/stable/1.2/qiskit/circuit/library).

    ​For each folder, the following types of files are included.

+ `xxx.py`:

  The raw version of each quantum program,  where `xxx` refers to the name of the object program (i.e., `Id`, `comp`, `linear`, `quad`, `qft` and `adder`).  

+ `xxx_circuit_info.py`:

  This file is used to collect basic information (# Qubits, # Gates and #Depths) of the quantum circuit corresponding to each program version. The relevant results are displayed in Table 2 of the manuscript.

+ `xxx_specification.py`:

  This file calculates the expected output distribution according to the formula-based program specification provided by Qiskit. The functions `PSTC_specification` and `MSTC_specification` respectively correspond to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).

+ `xxx_versions_info.md`:

  This file details the manually implanted bugs mentioned in Table 2 of the manuscript.

+ `xxx_defecti.py`:

  The buggy version mutated from the raw one. `i` indicates the name of the buggy version. For example, `adder_defect2.py` is the `v2` of the object `WA`.

+ `xxx_RQj.py`:

  This file implements the experiment for RQ`j`, where `j`=1, 2, 3, 4 and 5. **When replicating the experiment, please run this file directly**.

## Files of executable functions

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
