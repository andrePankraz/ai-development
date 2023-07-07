# This file was created by ]init[ AG 2023.
#
# see https://hub.docker.com/r/nvidia/cuda/tags?page=1&name=11.8.0-cudnn8-devel-ubuntu22.0
FROM harbor.init.de/docker.io/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS base
VOLUME /tmp
ARG DEBIAN_FRONTEND=noninteractive
ENV DEB_PYTHON_INSTALL_LAYOUT=deb_system
RUN apt-get update -y && \
  apt-get install -y git python3-pip && \
  python3 -m pip install --upgrade pip
# see https://pytorch.org/get-started/locally/
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip3 install \
  torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

WORKDIR /opt/ai_development
COPY pyproject.toml .
COPY setup.py .
COPY README.md .
COPY src ./src

FROM base AS dev
RUN pip3 install --editable .[dev]

FROM base AS local
COPY LICENSE .
RUN pip3 install --editable .
CMD ["uvicorn", "ai_development.service:app", "--host", "0.0.0.0", "--port", "8200"]
