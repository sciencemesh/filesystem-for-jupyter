# main, official image

# https://github.com/jupyterhub/helm-chart
ARG Z2JH_HELM_VERSION=1.1.3
# https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/hub
FROM jupyterhub/k8s-hub:$Z2JH_HELM_VERSION AS jupyterhub-official

USER root

# add our template directory
COPY templates /opt/templates

# add nextcloud_spawner
COPY nextcloud_spawner /opt/nextcloud_spawner
RUN pip3 install /opt/nextcloud_spawner

# switching back to the default user of the base image
USER jovyan

###
###
###

# extended image for local development
FROM jupyterhub-official AS jupyterhub-dev

USER root

# installing dependencies for running the http proxy and the notebook server locally
RUN apt-get update && \
    curl -sL https://deb.nodesource.com/setup_14.x -o /tmp/nodesource_setup.sh && \
    bash /tmp/nodesource_setup.sh && \
    rm /tmp/nodesource_setup.sh && \
    apt-get install -y nodejs && \
    npm install -g configurable-http-proxy && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install \
        notebook==5.7.10

# add dev configuration
COPY docker/dev_jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

# switching back to the default user of the base image
USER jovyan
