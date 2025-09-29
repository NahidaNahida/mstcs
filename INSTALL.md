# Setup Environment

The instructions include two alternatives for setup, one using Anaconda to install all packages listed in [`requirements.txt`](./requirements.txt), and the other pulling the Docker image available at [our repository](https://github.com/NahidaNahida/mstcs/pkgs/container/mstcs-container) to replicate the same environment used in our previous experiments. 

## Anaconda

This manner employs Anaconda to create a virtual environment manually. First, we create an environment named `mstcs` with `python=3.11.0`.

```bash
conda create --name mstcs python=3.11.0
```

Then, activate it through

```bash
conda activate mstcs
```

Upon changing the directory to `mstcs`, download the required packages based on [requirements.txt](https://github.com/NahidaNahida/mstcs/blob/main/requirements.txt),

```bash
conda install --file requirements.txt
```

If some packages are not available from current channels,  we can still try Python Package Installer (i.e., `pip install`) repository as a compromised solution through

```bash
pip install -r requirements.txt
```

By following all the above steps, it is ready to run the code and replicate the results in the conda environment `mstcs`.

## Docker

As an alternative, we also release the docker image, such that the docker container can be directly used to replicate the environment. For more details about docker, please refer to the [web](https://www.docker.com/).

To begin with, we pull the package by

```bash
docker pull ghcr.io/nahidanahida/mstcs-container:latest
```

Then, we should build a container based on the pulled Docker image. The container will include a volume mount that binds the target directory (i.e., that of the cloned `mstcs`) to a specific path inside the container. This ensures that any changes made in the host's `mstcs` are reflected within the container, enabling seamless interaction with the local development environment. In general, we are supposed to run the following command,

```bash
docker run `
  -p <HOST_PORT>:<CONTAINER_PORT> `
  -it --platform linux/amd64 `
  --name mstcs-container `
  -v "<HOST_PATH>:<CONTAINER_PATH>" `
  ghcr.io/nahidanahida/mstcs-container:latest `
  /bin/bash
```

where, 

+ `HOST_PORT` and `CONTAINER_PORT`: 8888:8888
+ `HOST_PATH`: The path of the repository `mstcs` in your computer or server (e.g., the template  like `.../mstcs`).
+ `CONTAINER_PATH`: The path set for the container (e.g., `/app`).

Congratulations! You are ready to run the code and replicate the results.

By the way, if the container has already existed, we can run the following command to step into the container.

```bash
docker start mstcs-container
docker exec -it mstcs-container /bin/bash
```

