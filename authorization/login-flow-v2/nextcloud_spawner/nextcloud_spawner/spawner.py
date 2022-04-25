import os

from jupyterhub.spawner import SimpleLocalProcessSpawner
from kubespawner import KubeSpawner

from .credentials import NcCredentials, NcAuthorizationFlow
from .nc_handler import NextcloudFilesystemHandlerContainer
from .messages import getmsg

# just checking if it's set because it's needed
os.environ['JUPYTERHUB_CRYPT_KEY']
NC_URL = os.environ['NC_URL']


class NextcloudSpawnerMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nc_url = NC_URL
        self._nc_authorization_flow = None
        self._reset_nc_authorization_flow()

    def options_form(self, _):
        """ Returns a HTML form if NC grant is needed. None otherwise. """
        if self._has_valid_nc_credentials():
            self.log.info('NC credentials already stored in the database')
            return None

        return {
            'authorization_url': self._nc_authorization_flow.get_authorization_url(),
        }

    def options_from_form(self, form_data):
        """ Validates the form
        i.e. raises error if NC grant is not completed
        or returns NC credentials to be stored in db (encrypted!), once it's completed.

        Form data comes as a dict of lists of strings.
        """
        if form_data.get('reset_authorization_flow', False):
            self._reset_nc_authorization_flow()
            raise Exception(getmsg('NC_AUTHZ_FLOW_RESET_DONE'))

        nc_credentials = self._try_reading_credentials_from_nc()
        if nc_credentials:
            # returned data will be saved in the Hub db
            return nc_credentials.to_encrypted_dict()
        else:
            raise Exception(getmsg('NO_NC_GRANT'))

    def pre_spawn_hook(self, _):
        if not hasattr(self, 'extra_containers'):
            self.log.error('The spawner is %s, and it has no extra_containers field. ' +
                           'Not in K8S? Nextcloudcmd WILL NOT be run!', self)
            return

        try:
            handler_container = NextcloudFilesystemHandlerContainer(self._get_stored_nc_credentials(), self.volume_mounts)
            extra_container = handler_container.to_extra_container_dict()
            self._add_extra_container(extra_container)
        except NcCredentials.DeserializationError:
            # illegal state
            self.log.error('NC credentials cannot be read from user_options. The options are: %s' % self.user_options)
            raise Exception(getmsg('NC_CREDENTIALS_DESERIALIZATION_ERROR'))

    def _add_extra_container(self, extra_container):
        new_list = []

        # skip previous duplicate(s) of the newly-added container
        for existing in self.extra_containers:
            if extra_container['name'] != existing.get('name', None):
                new_list.append(existing)

        new_list.append(extra_container)
        self.extra_containers = new_list

    def _has_valid_nc_credentials(self):
        try:
            nc_credentials = self._get_stored_nc_credentials()
            return self._nc_authorization_flow.check_credentials_are_valid(nc_credentials)
        except NcCredentials.DeserializationError:
            return False

    def _get_stored_nc_credentials(self):
        return NcCredentials.from_encrypted_dict(self._get_stored_user_options())

    def _try_reading_credentials_from_nc(self):
        try:
            nc_credentials = self._nc_authorization_flow.read_credentials()
            self.log.info('NC credentials successfully obtained!')
            return nc_credentials
        except NcAuthorizationFlow.CredentialsNotYetAvailable:
            self.log.info('NC credentials not yet available in NC!')
            return None

    def _reset_nc_authorization_flow(self):
        self._nc_authorization_flow = NcAuthorizationFlow(nc_url=self.nc_url)

    def _get_stored_user_options(self):
        return self.orm_spawner.user_options or {}


class NextcloudLocalProcessSpawner(NextcloudSpawnerMixin, SimpleLocalProcessSpawner):
    pass


class NextcloudKubeSpawner(NextcloudSpawnerMixin, KubeSpawner):
    pass
