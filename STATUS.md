# Badges

We aim for our artifact to be available, functional, and reusable.

## Available

The artifacts is available in this Github repository and archived on Zenodo. For future research of software engineering community, we use an open-source `MIT` license.

## Functional

+ Document: The `README.md` file documents the overview of the entire artifact and details for each files. The code includes necessary code comments to ensure the readability and interpretability.
+ Consistent: 
+ Complete:
+ Exercisable: 

We provide a Singularity definition file for each experiment, which automates experiment preparation. The `README.md` file precisely documents all necessary manual steps. We have successfully tested and confirmed functionality on three different machines.

## Reusable

This repository includes detailed steps on how to use the artifacts and reproduce the experiments in the `REQUIREMENTS.md`, `INSTALLL.md`, and `README.md` files. We have structured our project modularly, making the FlowFuzz tool independent of the subjects. By separating the experiments into containers, reusability is ensured. All dependencies are automatically installed and prepared during the image build process, keeping the usage simple. Additionally, we provide a template project and instructions in the `README.md`, offering an easy starting point for adding new subjects.