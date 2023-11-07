# This file was created by ]init[ AG 2023.
#
# see https://hub.docker.com/r/nvidia/cuda/tags?page=1&name=cudnn8-devel-ubuntu22.0
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS base

ARG DEBIAN_FRONTEND=noninteractive
ENV DEB_PYTHON_INSTALL_LAYOUT=deb_system
RUN apt-get update && \
  apt-get full-upgrade -y && \
  apt-get install -y tzdata && \
  ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
  dpkg-reconfigure --frontend noninteractive tzdata && \
  apt-get install -y curl git python3-pip && \
  python3 -m pip install --upgrade pip && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# see https://pytorch.org/get-started/locally/
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip3 install \
  torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

WORKDIR /opt/ai_development
COPY pyproject.toml .
COPY setup.py .
COPY README.md .
COPY src ./src

EXPOSE 8200

FROM base AS dev
RUN pip3 install --editable .[dev]

FROM base AS local
COPY LICENSE .
RUN pip3 install .
# VOLUME /opt/ai_development/data
CMD ["uvicorn", "ai_development.service:app", "--host", "0.0.0.0", "--port", "8200", "--log-level", "warning"]
HEALTHCHECK --interval=5s --timeout=5s --retries=5 CMD curl --include --request GET http://localhost:8200/health || exit 1
