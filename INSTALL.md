# Setup Environment

The instructions include two alternatives for setup, one using Anaconda to install all packages listed in [`requirements.txt`](./requirements.txt), and the other pulling the Docker image available at [our repository](https://github.com/NahidaNahida/mstcs/pkgs/container/mstcs-container) to replicate the same environment used in our previous experiments. 

## Anaconda

This manner employs Anaconda to create a virtual environment manually. First, we create an environment named `mstcs` with Python 3.11.0 by

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

If some packages are not available from the current channels, we can still try Python Package Installer as a compromised solution through

```bash
pip install -r requirements.txt
```

By following all the above steps, it is ready to run the code and replicate the results in the conda environment `mstcs`.

## Docker

If practitioners are familiar with Docker, we would strongly recommend this method to clone an environment identical to the one we previously used, without any unexpected issues. For more details about docker, please refer to the [web](https://www.docker.com/).

To begin with, we start Docker Desktop and pull the package by

```bash
docker pull ghcr.io/nahidanahida/mstcs-container:latest
```

Then, we should build a container based on the pulled Docker image. The container will include a volume mount that binds the target directory (i.e., that of the cloned or downloaded `mstcs`) to a specific path inside the container. This ensures that any changes made in the host's `mstcs` are reflected within the container, enabling seamless interaction with the local development environment. In general, we are supposed to run the following command,

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

+ `<HOST_PORT>` and `<CONTAINER_PORT>`: The two arguments refer to the ports for the host and the built container, respectively. For instance, we can set both ports `<HOST_PORT>` and `<CONTAINER_PORT>` as 8888.
+ `<HOST_PATH>` and `<CONTAINER_PATH>`: The former indicates the intended absolute path of the repository `mstcs` in the local computer or the remote server (e.g., in the form of `./mstcs`), while the latter refers to the path inside the container (e.g., `/app`).

After finishing the above steps, we can run the code within the established container named `mstcs−container`. By the way, if such a container has already been built, we can straightforwardly run the following two commands to step into the container:

```bash
docker start mstcs-container
docker exec -it mstcs-container /bin/bash
```
