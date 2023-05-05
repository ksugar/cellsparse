FROM tensorflow/tensorflow:2.12.0-gpu-jupyter

LABEL maintainer="ko.sugawara@riken.fr"

ARG NVIDIA_DRIVER_VERSION=530

RUN curl -OL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb \
 && dpkg -i cuda-keyring_1.0-1_all.deb && rm cuda-keyring_1.0-1_all.deb \
 && rm /etc/apt/sources.list.d/cuda.list

# Install StarDist and its dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ocl-icd-dev \
    ocl-icd-opencl-dev \
    opencl-headers \
    clinfo \
#    libnvidia-compute-${NVIDIA_DRIVER_VERSION} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install gputools edt
COPY stardist-sparse /tmp/stardist-sparse
RUN python3 -m pip install /tmp/stardist-sparse && rm -r /tmp/stardist-sparse

# Install Cellpose
COPY cellpose-sparse /tmp/cellpose-sparse
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install /tmp/cellpose-sparse && rm -r /tmp/cellpose-sparse

# Install ELEPHANT and its dependencies
COPY elephant-server/elephant-core /tmp/elephant-core
RUN python3 -m pip install zarr pika redis
RUN python3 -m pip install /tmp/elephant-core && rm -r /tmp/elephant-core

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/notebook --ip 0.0.0.0 --no-browser --allow-root"]