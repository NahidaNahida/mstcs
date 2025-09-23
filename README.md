# mstcs 
MSTCs (i.e., mixed-state test cases) is a new concept proposed in our paper. It suggests preparing and utilizing mixed states as the test inputs for quantum programs, since the mixed states have the power to represent multiple pure states in a probabilistic combination. Therefore, an MSTC demonstrates a higher input domain coverage than a PSTC (i.e., pure-state test cases) that are widely discussed in existing works, thereby contributing to the test effectiveness and efficiency. The empirical evaluation of MSTCs is based on the quantum software development kit Qiskit, and the backend is selected as an ideal simulator. For more details, please refer to our paper.

## Publication

This repository includes the all code and data involved in our paper "*Preparation and Utilization of Mixed States for Testing Quantum Programs*" that has been accepted as a journal-first article at ACM Transactions on Software Engineering and Methodology (TOSEM). 

```
Li Y, Cai K Y, Yin B. Preparation and Utilization of Mixed States for Testing Quantum Programs[J]. ACM Transactions on Software Engineering and Methodology, 2025. 
```

Paper link: [https://dl.acm.org/doi/abs/10.1145/3736757](https://dl.acm.org/doi/abs/10.1145/3736757).

The archived version of this artifact can be found in [https://zenodo.org/records/15462299](https://zenodo.org/records/15462299).

## Steps for Replication

### Getting Started

1. Use the following commend line to clone this repository.

   ```
   git clone https://github.com/NahidaNahida/mstcs.git
   ```

2. Set up the environment instructed by [INSTALL.md](https://github.com/NahidaNahida/mstcs/blob/main/INSTALL.md).

Note: We also provide an available [docker image](https://github.com/NahidaNahida/mstcs/pkgs/container/mstcs-container) with Linux/amd64, which will contain all you need to run the code (Python files along with Jupyter notebooks) in this artifact.

### Running for RQs

We offer a running example to replicate the empirical results for involved object programs and research questions. We include a separate file [`run.py`](./mycode/run.py) as a port to receive the commend and execute the corresponding experiment. First, change the directory to the root `\mstc` (a.k.a. the directory of this `README` file) and run the following command,

```bat
python -m mycode.run --program [PROGRAM] --rq [RQ_INDEX] --mode [REP_MODE]
```

where, 

+ `PROGRAM` (necessary argument):  The abbreviation of the object program, i.e., 
  + `id` for `Identity` $(\texttt{Id})$;
  + `comp` for `IntegerComparator` $(\texttt{IC})$;
  + `amplitude` for `LinearAmplitudeFunction`  $(\texttt{LAF})$;
  + `pauli` for `LinearPauliRotations`  $(\texttt{LPR})$; 
  + `quad` for `QuadraticForm`  $(\texttt{QF})$;
  + `qft` for `QuantumFourierTransform`  $(\texttt{QFT})$; 
  + `adder` for `WeightedAdder`  $(\texttt{WA})$.
+ `RQ_INDEX` (necessary argument): The index of the research question (i.e., `1`, `2`, `3`, `4`, `5`, and `6`).
+ `REP_MODE` (unnecessary argument): The mode for replication. Herein, we provide two modes: `toy` and `all`. The mode `toy` only executes a small subset of the raw test suites for the feasibility of examining the artifact's functionality within an affordable time budget. Meanwhile, the mode `all` indicates to execute all the test suites involved in our TOSEM paper. For convenience, the above command without `--mode [REP_MODE]` still works, which stands for the default `all` mode.

Herein, we offer an example to run the experiment, i.e.,

```bat
python run_experiment.py --program comp --rq 2 --mode toy
```

which intends to run RQ2 of $\texttt{IC}$ upon the `toy` model. 

### Saving the Results

The yielded results (stored as a `.csv` file) are saved to `./data/raw_data_for_empirical_results/RQ/PROGRAM` automatically.



### Data Analysis

This repository includes two notebooks:

+ `motivational_example.ipynb`: run and analyze a toy example of `WA-v4` as the motivation of proposing MSTCs.
+ `drawing_figures.ipynb`: replicate the figures (Fig.10 and Fig.11) involved in the empirical studies.  

To run the notebook, you can use the following commend,

```
jupyter notebook --allow-root --ip=0.0.0.0 --NotebookApp.token=''
```

Then, the link that the Jupyter Server is running at will be returned. Through that, you can visit the notebook in the host browser.

## Data Availability

### Benchmark and Info Collection

In the file `code`, there are 7 folders (i.e., `Identity`, `IntegerComparator`, `LinearPauli Rotations`, `LinearAmplitudeFunction`, `QuadraticForm`, `QuantumFourier Transform` and `WeightedAdder`) that correspond to the object programs used in the manuscript. These 6 real-world quantum programs (except `Identity` of the above 7) can be found at `qiskit.circuit.library` (https://github.com/Qiskit/qiskit/tree/stable/1.2/qiskit/circuit/library).

For each folder, the following types of files are included.

+ `xxx.py`: The raw version of each quantum program.

+ `xxx_circuit_info.py`: This file is used to collect basic information (# Qubits, # Gates and Depths) of the quantum circuit corresponding to each program version. The relevant results are displayed in Table 3 of the manuscript.

+ `xxx_specification.py`: This file calculates the expected output distribution according to the formula-based program specification provided by Qiskit. The functions `PSTC_specification` and `MSTC_specification` respectively correspond to pure-state test cases  and mixed-state test cases.

+ `xxx_versions_info.md`: This file details the manually implanted bugs mentioned in Table 3 of the manuscript.

+ `xxx_defectii.py`: The buggy version mutated from the raw one. `ii` indicates the name of the buggy version. For example, `adder_defect2.py` is the `v2` of the object `WA`.

+ `xxx_RQjj.py`: This file implements the experiment for RQ`jj`, where `jj`=1, 2, 3, 4, 5 and 6. When running `run.py`, this file is executed. 

### Experimental Results

We present all the raw data in the folder `data`. There are four folders within `data`:

+ `motivational_examples`: includes quantum circuit diagrams and results of testing `WA-v4` reported in the motivational example.
+ `plotting_for_empirical_results`: encompasses all the figures displayed in empirical studies, where these figures can be generated by  `drawing_figures.ipynb`.
+ `processed_tables_for_empirical_studies`: includes the preprocessed data corresponding to the tables in RQ2, RQ3 and RQ4.
+ `raw_data_for_empirical_studies`: contain the raw data yielded from running `run.py` with the required arguments.

**Note that** replicating the experiments will replace the raw file, since the new and raw outputs share the same filename.

## Functional Documentation

There is the documentation of some specific functions.

+ `data_convertion.py`: This file is used for preprocessing of data.

  + `generate_numbers(n, m)`:  Generate all the n-digit m-ary numbers and store them at corresponding lists.

  + `output_prob(counts, n)`: The list of measurement results is transformed into corresponding probability.

+ `preparation_circuits.py`: This file includes several functions related to the quantum circuits for the preparation of control states and the controlled preparation of mixed states. These functions are mainly used for the experiments of RQ2 and RQ4. For more details, please refer to this file.

+ `circuit_execution.py`: This file aims to execute the quantum circuit. Upon the backend `qsam_simulator`, the dictionary of the measurement results can be yielded.

+ `repeat_until_success.py`: It is used to achieve the repeat-until-success (RUS) structure using Qiskit. The RUS structure is discussed in Section 6.2.1 (Separable Control States) of the manuscript.

+ `test_oracle.py`: The test oracle is included in this file. More particularly, output probability oracle (OPO) is employed for MSTCs, and the Mann-Whitney U test compares two sample groups.

+ `run.py`: The separate files for running the required experiment.
