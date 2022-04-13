# Nextcloud-authorization extension to JupyterHub

This component extends JupyterHub with a custom spawner and a spawn page template. 

JupyterHub obtains Nextcloud credentials (app password) by implementing 
[Nextcloud's Login Flow v2](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html#login-flow-v2).
To this end, during spawning, a user is requested to interactively grant the access to their Nextcloud files. 

The credentials are then stored encrypted in the Hub's database as `user_options`. 

Finally, the credentials are passed to the single-user server.

## Usage in Docker

Usage of this extension in JupyterHub Docker image is implemented in [docker](docker).

This is also the easiest way to test the extension.

## Usage in general

JupyterHub must be configured to use the custom spawner and the custom template, as follows. 

In your JupyterHub environment, install the Python package with the custom spawner:

```
pip install <path to this 'nextcloud_spawner' directory>
```

Then in `jupyterhub_config.py`, choose the spawner class and the templates:

```
c.JupyterHub.spawner_class = 'nextcloud_spawner.NextcloudKubeSpawner'
c.JupyterHub.template_paths = ['/opt/templates']  # path to this 'templates' directory
```

Set the environmental variables for JupyterHub:
- `NC_HANDLER_IMAGE` - Docker image to be run as extra container within
the single-user pod, e.g. [nextcloudcmd image](../../sync) 
- `NC_URL` - Nextcloud URL, e.g. `https://drive.example.com/`
- `NC_REMOTE_DIR` - user directory in Nextcloud to be synchronized; 
empty string for user root directory
- `NC_LOCAL_DIR` - user directory in Jupyter to be synchronized; default: `/home/jovyan`
- `NC_INTERVAL` - delay in seconds between subsequent synchronizations (optional, default: 10)
- `NC_JUPYTER_LABEL` - name of the JupyterHub instance to be presented to Nextcloud
(will be seen in Nextcloud user profile in app passwords) 
- `JUPYTERHUB_CRYPT_KEY` - crypt key as expected by JupyterHub; 
for instance, generate with something like `$(openssl rand -hex 32)`

## Implementation details

The custom spawner is implemented as subclasses of KubeSpawner (intended for production) 
as well as SimpleLocalProcessSpawner (for testing purposes). 
See [here](nextcloud_spawner/nextcloud_spawner/__init__.py).

The subclass of KubeSpawner runs an extra container from the `$NC_HANDLER_IMAGE` within the single-user pod.
The image can be [nextcloudcmd image](../../sync).
The extra container shares the user home directory with the single-user server container,
so this allows syncing.

Tested with JupyterHub 1.1 and KubeSpawner 0.11.
