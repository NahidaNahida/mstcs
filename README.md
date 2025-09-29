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
python -m mycode.run --program <PROGRAM> --rq <RQ_IDX> --mode <REP_MODE>
```

where, 

+ `<PROGRAM>` (necessary argument):  The abbreviation of the object program, i.e., 
  + `id` for `Identity` $(\texttt{Id})$;
  + `comp` for `IntegerComparator` $(\texttt{IC})$;
  + `amplitude` for `LinearAmplitudeFunction`  $(\texttt{LAF})$;
  + `pauli` for `LinearPauliRotations`  $(\texttt{LPR})$; 
  + `quad` for `QuadraticForm`  $(\texttt{QF})$;
  + `qft` for `QuantumFourierTransform`  $(\texttt{QFT})$; 
  + `adder` for `WeightedAdder`  $(\texttt{WA})$.
+ `RQ_INDEX` (necessary argument): The index of the research question (i.e., `1`, `2`, `3`, `4`, and `5`).
+ `REP_MODE` (unnecessary argument): The mode for replication. Herein, we provide two modes: `toy` and `all`. The mode `toy` only executes a small subset of the raw test suites for the feasibility of examining the artifact's functionality within an affordable time budget. Meanwhile, the mode `all` indicates to execute all the test suites involved in our TOSEM paper. For convenience, the above command without `--mode [REP_MODE]` still works, which stands for the default `all` mode.

Herein, we offer an example to run the experiment, i.e., `python -m mycode.run --program comp --rq 2 --mode toy`, which intends to run RQ2 of $\texttt{IC}$ upon the `toy` model. 

### Saving the Results

The yielded results (stored as a `.csv` file) are saved to `./data/raw_data_for_empirical_results/RQ/PROGRAM` automatically.



### Data Analysis

This repository includes two notebooks:

+ `motivational_example.ipynb`: run and analyze a toy example of `WA-v4` as the motivation of proposing MSTCs.
+ `drawing_figures.ipynb`: replicate the figures (Fig.10 and Fig.11) involved in the empirical studies.  

To run the notebook, you can use the following commend,

+ For Jupyter Notebook interface configured by `NotebookApp`:

  ```bat
  jupyter notebook --allow-root --ip=0.0.0.0 --NotebookApp.token=''
  ```

+ For Jupyter Lab interface configured by `ServerApp`:

  ```bat
  jupyter lab --allow-root --ip=0.0.0.0 --ServerApp.token='' --ServerApp.password=''
  ```

Then, the link that the Jupyter Server is running at will be returned. Through that, you can visit the notebook in the host browser.
