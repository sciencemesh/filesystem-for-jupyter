# FUSE mount via webDAV

This Docker image makes a FUSE mount, in Jupyter, of EFSS files accessed via webDAV.

This Docker image is a Jupyter's single-user image.
The base image comes from [Zero to JupyterHub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/singleuser-sample). 

## Configure

The image is configured with the following environment variables:

* WEBDAV_ENDPOINT - WebDAV endpoint, pointing at a remote directory 
* WEBDAV_USER - username
* WEBDAV_PASS - password
* WEBDAV_LOCAL_DIR - local directory, within the user's home directory, 
to mount the remote files 

See examples below. 

## Build

```
docker build -t davfs .
```

## Run

It requires to be run as privileged container or with `SYS_ADMIN` capability.
It also requires the access to `/dev/fuse` on the Docker host.

For instance:

```
docker run \
    --cap-add SYS_ADMIN \
    --device /dev/fuse \
    -p 8888:8888 \
    -e JUPYTER_ENABLE_LAB=true \
    -e WEBDAV_ENDPOINT=https://drive.example.com/remote.php/dav/files/user/ \
    -e WEBDAV_USER=user \
    -e WEBDAV_PASS=secret123 \
    -e WEBDAV_LOCAL_DIR=drive \
    davfs
```

Notes:
* It runs a regular Jupyter notebook server. Check logs to access the user interface.
* The home directory is `/home/jovyan`, so the remote files will be mounted to `/home/jovyan/drive`.
* `JUPYTER_ENABLE_LAB` is the base image's config option to enable the JupyterLab user interface.

## OAuth2

This image can be tweaked, so accessing EFSS files is authorized with OAuth2 access token (instead of user&pass).
However, refreshing token is not supported yet (see #7).

First, obtain the access token. The example flow for Nextcloud:

```
# Add OAuth client in Nextcloud settings: /settings/admin/security
# You get $CLIENT_ID and $CLIENT_SECRET

curl https://$NC_DOMAIN/apps/oauth2/authorize?response_type=code&client_id=$CLIEND_ID&redirect_uri=http://localhost/test
# Go to URL returned in 'Location', and authorize client
# You get $CODE from the URL after redirection

curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=authorization_code&code=$CODE&redirect_uri=http://localhost/test&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET" https://$NC_DOMAIN/apps/oauth2/api/v1/token
# You get sth like: {"access_token":"...","token_type":"Bearer","expires_in":3600,"refresh_token":"...","user_id":"..."}
# The access_token is what we need later.
```

Then, tweak the image. 
Append `davfs2.conf` with:
```
add_header Authorization "Bearer ACCESS_TOKEN"
ask_auth 0
``` 

and rebuild the image.

Run the container with any non-empty values in `WEBDAV_USER` and `WEBDAV_PASS`.
