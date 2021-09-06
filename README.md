# EFSS Filesystem for Jupyter

This repo contains solutions for accessing user files stored in 
[EFSS](https://en.wikipedia.org/wiki/Enterprise_file_synchronization_and_sharing)
from [Jupyter ecosystem](https://jupyter.org/).

To this end, two issues, independent to some extent, are covered:

1. How to actually access user files from Jupyter
2. How to authorize Jupyter to access the files

By the Jupyter ecosystem, 
we mean specifically the following single-user components:

- [JupyterLab](https://github.com/jupyterlab/jupyterlab) UI
- JupyterLab Terminal
- Jupyter kernels, i.e. kernels that are local to JupyterLab, as well as remote 
[Jupyter Enterprise Gateway](https://jupyter-enterprise-gateway.readthedocs.io/)'s kernels
(in the future)

As EFSS, we use [Nextcloud](https://nextcloud.com/) (hereinafter as NC), tested with NC v. 16 and 17. 
The ultimate goal is to make this work independent from EFSS vendor. 

## File access

Alternative solutions for accessing files are:

- [sync](sync) - synchronize files with EFSS client
- [fuse](fuse) - FUSE mount EFSS files via webDAV

## Authorization

Solutions for authorizing Jupyter components to access Nextcloud:

- [authorization/login-flow-v2](authorization/login-flow-v2) - JupyterHub implementing Nextcloud's 
[Login Flow v2](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html#login-flow-v2)

## Usage examples

Some comprehensive usage examples:

- [examples/z2jh-sync](examples/z2jh-sync) - the sync and login-flow-v2 approaches
implemented within [Zero To JupyterHub](https://zero-to-jupyterhub.readthedocs.io/)
- [examples/z2jh-cs3api4lab-sync](examples/z2jh-cs3api4lab-sync) - the sync and login-flow-v2 approaches
implemented within [Zero To JupyterHub](https://zero-to-jupyterhub.readthedocs.io/)
together with [the cs3api4lab plugin](https://github.com/sciencemesh/cs3api4lab)

## Docker images

Docker images defined in this repo are automatically built and published in 
[GitHub Packages registry](https://github.com/sciencemesh/filesystem-for-jupyter/packages).

The Docker images are:
```
docker.pkg.github.com/sciencemesh/filesystem-for-jupyter/jupyterhub
docker.pkg.github.com/sciencemesh/filesystem-for-jupyter/sync
```

[Read here](https://docs.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages)
how to access the registry.
