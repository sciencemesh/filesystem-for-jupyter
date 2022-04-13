import os

NC_URL = os.environ['NC_URL']
NC_HANDLER_IMAGE = os.environ['NC_HANDLER_IMAGE']
NC_REMOTE_DIR = os.environ['NC_REMOTE_DIR']
NC_LOCAL_DIR = os.environ.get('NC_LOCAL_DIR', '/home/jovyan')
NC_INTERVAL = os.environ.get('NC_INTERVAL', '10')


class NextcloudFilesystemHandlerContainer:
    """ Defines the handler container,
    i.e. the extra container responsible for providing Nextcloud filesystem to Jupyter,
    e.g. Nextcloudcmd - the Nextcloud sync client
    """

    def __init__(self, nc_credentials, volume_mounts):
        """
        :param nc_credentials: instance of NcCredentials
        :param volume_mounts: volume mounts in the format of KubeSpawner.volume_mounts
        """
        self.nc_credentials = nc_credentials
        self.volume_mounts = volume_mounts

        self.nc_url = NC_URL
        self.nc_handler_image = NC_HANDLER_IMAGE
        self.nc_remote_dir = NC_REMOTE_DIR
        self.nc_local_dir = NC_LOCAL_DIR
        self.nc_interval = NC_INTERVAL

    def to_extra_container_dict(self):
        return {
            'name': 'nc-handler',
            'image': self.nc_handler_image,
            'volumeMounts': self.volume_mounts,
            'env': self._build_k8s_env_dict(),
        }

    def _build_k8s_env_dict(self):
        env_list = list()
        for name, value in self._get_raw_env().items():
            env_list.append({
                'name': name,
                'value': value,
            })
        return env_list

    def _get_raw_env(self):
        return {
            'NC_URL': self.nc_url,
            'NC_REMOTE_DIR': self.nc_remote_dir,
            'NC_LOCAL_DIR': self.nc_local_dir,
            'NC_USER': self.nc_credentials.user,
            'NC_PASS': self.nc_credentials.password,
            'NC_INTERVAL': self.nc_interval,
        }
