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

1. Use the following command to clone this repository.

   ```bash
   git clone https://github.com/NahidaNahida/mstcs.git
   ```

2. Set up the environment instructed by [INSTALL.md](https://github.com/NahidaNahida/mstcs/blob/main/INSTALL.md).

Note: We also provide an available [docker image](https://github.com/NahidaNahida/mstcs/pkgs/container/mstcs-container) with Linux/amd64, which will contain all you need to run the code (Python files along with Jupyter notebooks) in this artifact.

### Running for RQs

We offer a running example to replicate the empirical results for involved object programs and research questions. We adopt a separate file [`run.py`](./mycode/run.py) as a port to receive the command and execute the corresponding experiment. First, change the directory to the root `\mstc` (a.k.a. the directory of this `README` file) and run the following command,

```bash
python -m mycode.run --program <PROG_SHORT> --rq <RQ_IDX> --mode <REP_MODE>
```

where, 

+ `<PROG_SHORT>` (necessary argument):  This is an argument indicating the lowercase abbreviation of the object program, i.e., 
  + `id` for `Identity` $(\texttt{Id})$;
  + `comp` for `IntegerComparator` $(\texttt{IC})$;
  + `amplitude` for `LinearAmplitudeFunction`  $(\texttt{LAF})$;
  + `pauli` for `LinearPauliRotations`  $(\texttt{LPR})$; 
  + `quad` for `QuadraticForm`  $(\texttt{QF})$;
  + `qft` for `QuantumFourierTransform`  $(\texttt{QFT})$; 
  + `adder` for `WeightedAdder`  $(\texttt{WA})$.
+ `<RQ_INDEX>` (necessary argument): The index of the research question. There are five valid arguments at most, i.e., `1`, `2`, `3`, `4`, and `5`. Unlike the six real-world programs, the benchmark program $\texttt{Id}$ is not employed in the three experiments that discuss test effectiveness, so only `1` and `2` are valid for $\texttt{Id}$.
+ `<REP_MODE>` (unnecessary argument): The mode for replication. Herein, we provide two modes: `toy` and `all`. The mode `toy` only executes a small configurable subset of the raw test suites for the feasibility of examining the artifact’s functionality within an affordable time budget. Meanwhile, the mode `all` indicates executing all the test suites involved in our article, whereas it might take several days to finish traversing all the RQs for each of the QPs. Besides, for convenience, the above command without `−−mode <REP_MODE>` still works, which indicates the default `all` mode.

We offer an example to run the experiment, i.e., `python -m mycode.run --program comp --rq 2 --mode toy`, which intends to run RQ2 of $\texttt{IC}$ upon the `toy` model. 

### Data Analysis

This repository includes two notebooks:

+ `motivational_example.ipynb`: Through this notebook, we can run and analyze a toy example of `WA-v4` introduced as the motivation for proposing MSTCs. Especially, this notebook prints the test results of executing all PSTCs and draws quantum circuits of the program version under test. More details about the example can be found in Section 4 of our TOSEM paper. The generated test results and quantum circuit diagrams will be saved in the directory `mstcs/<SAVE_MODE>/motivational_examples`.
+ `drawing_figures.ipynb`: It aims to reproduce two figures (i.e., Fig. 10 for RQ1 and Fig. 11 for RQ5) involved in empirical studies. Note that its successful work relies on the complete results produced from the all mode. Still, we can test the functionality of this notebook based on the raw data offered in the folder `rawdata`. The produced figures will be saved in the directory `mstcs/<SAVE_MODE>/plotting_for_empirical_results`.

If we intend to run Jupyter notebooks within the container `mstcs−container`, then run one of the following two alternatives,

+ For Jupyter Notebook interface configured by `NotebookApp`:

  ```bat
  jupyter notebook --allow-root --ip=0.0.0.0 --NotebookApp.token=''
  ```

+ For Jupyter Lab interface configured by `ServerApp`:

  ```bat
  jupyter lab --allow-root --ip=0.0.0.0 --ServerApp.token='' --ServerApp.password=''
  ```

After that, the link that the Jupyter Server is running at will be returned in the terminal log. Then, we can visit the notebook in the host browser.
