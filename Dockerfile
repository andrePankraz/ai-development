# This file was created by ]init[ AG 2023.
#
# see https://hub.docker.com/r/nvidia/cuda/tags?page=1&name=cudnn8-devel-ubuntu22.0
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04 AS base

ARG DEBIAN_FRONTEND=noninteractive
ENV DEB_PYTHON_INSTALL_LAYOUT=deb_system
RUN apt-get update && \
	# Upgrade system
	apt-get full-upgrade -y && \
	# Install locale and timezone data, set timezone Berlin
	apt-get install -y locales tzdata && \
	locale-gen de_DE.UTF-8 && \
	ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \ 
	dpkg-reconfigure --frontend noninteractive tzdata && \
	# Curl, Git, Python & Pip
	apt-get install -y curl git python3-pip && \
	# Cleanup
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

# Set default locale de_DE.utf8
ENV LANG de_DE.utf8
ENV LC_ALL de_DE.utf8

# Update Pip & install Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install --upgrade pip setuptools poetry && \
	poetry config installer.max-workers 10

# see https://pytorch.org/get-started/locally/
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

WORKDIR /opt/ai-development
COPY pyproject.toml setup.py README.md ./
COPY src ./src

EXPOSE 8200

FROM base AS dev
ENV TARGET=dev
RUN pip3 install --editable .[dev]

FROM base AS run
ENV TARGET=run
COPY .env LICENSE ./
RUN pip3 install .

COPY start_services.sh .
RUN chmod +x start_services.sh
CMD ./start_services.sh
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD curl --include --request GET http://localhost:8200/health || exit 1
