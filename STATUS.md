# ACM Badges

Our artifacts aim to be available, functional, and reusable.

## Available

The artifacts are available in the [Github repository](https://github.com/NahidaNahida/mstcs) and archived on Zenodo. About the copyright, all the artifacts were released under the permissive MIT license.

## Functional

Regarding the functionality, our latest artifacts can be evaluated in the following aspects:

+ **Document**: The `README.md` file documents the overview of the entire artifact. The code includes necessary code comments and type hints to ensure the readability and interpretability.
+ **Consistent**: Although we refined the artifact with modularization adopted, we ensured that no code regression was introduced and no intended functionalities were removed. Therefore, our artifacts are consistent with what the publication claimed for the empirical studies.
+ **Complete**: Our artifacts can be used to replicate the results of 5 research questions for each involved program. A Jupyter notebook is also provided for data analysis, such as generating all the figures for empirical studies, which are displayed in the published paper. 
+ **Exercisable**: Our artifacts include a separate file `run.py` as a port to receive the command and run the corresponding experiment. The outputs are stored in `.csv` and saved at an assigned directory path.

## Reusable

Our artifacts include detailed steps on how to use the artifact and reproduce the experiments in the `README.md`, `requirements.txt`, and `INSTALL.md`. The `README.md` provides detailed instructions to clone and get start the artifact. For two approaches for setups documented in `INSTALL.md`, one creates the conda environment by installing the packages listed in `requirements.txt`, and the other utilizes the provided docker image to pull the container identical to what was used in the paper.  

Additionally, the artifacts comprise several utilities across different levels, designed not only to implement current test processes but also to enable iterative development and promote reuse. There are nine Python modules for global usage in the artifact, and three Python modules specific to each program under test. Some specific functions are documented well, where these functions are promised to be reused in the future work.