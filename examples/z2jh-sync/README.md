# Example for Z2JH

The sync and login-flow-v2 approaches implemented within 
[Zero To JupyterHub](https://zero-to-jupyterhub.readthedocs.io/) (Z2JH)
in Kubernetes.

Tested with [Z2JH charts](https://github.com/jupyterhub/helm-chart) 
v. 0.9.0 and 1.1.3.

Tested with Docker Engine and CRI-O.

## Setup

Latest Docker images built from this repo are used in this example. 
Make your Kubernetes able to pull the images.
Check section 'Docker images' in the main [README](../../README.md). 

Setup JupyterHub as [documented in Z2JH](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub/setup-jupyterhub.html),
adjusting `config.yaml` as given below.

For instance:

```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

helm upgrade --cleanup-on-fail \
  --install jhub jupyterhub/jupyterhub \
  --version=1.1.3 \
  --values config.yaml
```

Example for `config.yaml`:

```
proxy:
  # add the secretToken setting for the chart version < 1.0.0
  # generate with: `openssl rand -hex 32`
  # secretToken: 14836d60c5e9fe8a9c9e2cec7693687d6ba024f2593f01425f522e1d2525dba1
  https:
    enabled: false

hub:
  image:
    name: docker.pkg.github.com/sciencemesh/filesystem-for-jupyter/jupyterhub
    tag: latest
  templatePaths:
    # the custom templates added in the JupyterHub image
    - /opt/templates
  extraConfig:
    00-nextcloud-kube-spawner: |
       c.JupyterHub.spawner_class = 'nextcloud_spawner.NextcloudKubeSpawner'
  extraEnv:
    # `openssl rand -hex 32`
    JUPYTERHUB_CRYPT_KEY: 7757f14cbf7d4fd47939a559ef13110c460c535a4d3d87eb7c33d66c50473df8
    NC_HANDLER_IMAGE: docker.pkg.github.com/sciencemesh/filesystem-for-jupyter/sync:latest
    NC_URL: https://drive.example.com/
    NC_REMOTE_DIR: notebooks
    NC_JUPYTER_LABEL: Jupyter Test instance
```
