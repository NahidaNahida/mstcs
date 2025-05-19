# ACM Badges

This artifact aims to be available, functional, and reusable.

## Available

The artifact is available in the [Github repository](https://github.com/NahidaNahida/mstcs) and archived on Zenodo. For future research of quantum software engineering community, an open-source `MIT` license is used.

## Functional

Regarding the functionality, this artifact can be evaluated in the following aspects:

+ Document: The `README.md` file documents the overview of the entire artifact and details for each files. The code includes necessary code comments to ensure the readability and interpretability.
+ Consistent: This artifact is consistent with what the publication claimed for the empirical studies.
+ Complete: This artifact can be used to replicate the results of 5 research questions for each involved program. A Jupyter notebook is also provided to generate all the figures for empirical studies, which are displayed in the published paper.
+ Exercisable: This artifact includes a separate file `run.py` as a port to receive the commend and run the corresponding experiment. The outputs are stored in `.csv` and saved at an assigned directory path.

## Reusable

This artifact includes detailed steps on how to use the artifact and reproduce the experiments in the `README.md`, `requirements.txt`, and `INSTALLL.md`. The `README.md` provides detailed instructions to clone and get start the artifact. Additionally, some specific functions are documented well, where these functions are promised to be reused in the future work. The artifact suggest two manners to set up the environment. The one creates the conda environment by installing the packages listed in `requirements.txt`, and other utilizes the provided docker image to pull the container identical to what was used in the paper.  