# Setup Environment

## Anaconda

This manner employs Anaconda to create a virtual environment manually. First, we create an environment named `mstc` with `python=3.11.0`.

```
conda create --name mstcs python=3.11.0
```

Then, activate it through

```
conda activate mstcs
```

Upon changing the directory to `mstcs`, download the package based on the provided [requirements.txt](https://github.com/NahidaNahida/mstcs/blob/main/requirements.txt),

```
conda install --file requirements.txt
```

If some packages are not available from current channels, we can try `pip install` as a compromised solution.

```
pip install -r requirements.txt
```

Congratulations! You are ready to run the code and replicate the results.

## Docker

As an alternative, we also release the docker image, such that the docker container can be directly used to replicate the environment. 

First, we use docker to pull the package by

```bat
docker pull ghcr.io/nahidanahida/mstcs-container:latest
```

Then, start the container with a volume mount that binds the target directory (i.e., the cloned folder `mstcs`) to a path inside the container.

```bat
docker run -p 8888:8888 -it --platform linux/amd64 --name mstcs-container -v "[HOST_PATH]:[CONTAINER_PATH]" ghcr.io/nahidanahida/mstcs-container:latest /bin/bash
```

where, 

+ `HOST_PATH`: The directory path of the cloned `mstcs`.
+ `CONTAINER_PATH`: The path set for the container (e.g., `/app`).

Congratulations! You are ready to run the code and replicate the results.

By the way, if the image has already existed, we can run the following commend to step into the container.

```
docker start mstcs-container
docker exec -it mstcs-container /bin/bash
```
