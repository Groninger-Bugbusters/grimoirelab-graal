ARG PYTHON_VERSION=3.8
ARG FOSSOLOGY_VERSION="3.11.0"
ARG GOLANG_VERSION=1.17

FROM python:${PYTHON_VERSION}-buster

ARG FOSSOLOGY_VERSION
ARG GOLANG_VERSION

# # TZ required for non-interactive cmake installation
# ENV TZ=Etc/UTC
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get upgrade -y

# Install apt dependencies
RUN apt-get update && \
  apt-get -y install --no-install-recommends \
  bash locales \
  gcc \
  git git-core \
  build-essential \
  cmake \
  pkg-config \
  libicu-dev \
  zlib1g-dev \
  libcurl4-openssl-dev \
  libssl-dev \
  unzip curl wget sudo ssh \
  default-jre

# Install Ruby
RUN apt-get install -y --no-install-recommends \
  ruby-dev

# Install Go
RUN rm -rf /usr/local/go
RUN wget "https://dl.google.com/go/go$GOLANG_VERSION.linux-amd64.tar.gz" && tar -C /usr/local -xzf go$GOLANG_VERSION.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:/root/go/bin:${PATH}"
RUN rm go$GOLANG_VERSION.linux-amd64.tar.gz

WORKDIR /graal/exec
# Install Cloc
RUN apt-get install -y --no-install-recommends \
  cloc

# Install Fossology
RUN wget https://github.com/fossology/fossology/releases/download/$FOSSOLOGY_VERSION/FOSSology-$FOSSOLOGY_VERSION-debian-buster.tar.gz
RUN tar -xzf FOSSology-$FOSSOLOGY_VERSION-debian-buster.tar.gz
RUN apt-get -y install ./packages/fossology-common_$FOSSOLOGY_VERSION-1_amd64.deb ./packages/fossology-nomos_$FOSSOLOGY_VERSION-1_amd64.deb
RUN rm FOSSology-$FOSSOLOGY_VERSION-debian-buster.tar.gz

# Install Scc
RUN go install github.com/boyter/scc@91af61dfda0d9fa8f9a0c9f32ee204d5925b1bef

# Install Jadolint
RUN wget https://github.com/crossminer/crossJadolint/releases/download/Pre-releasev2/jadolint.jar

# Install Scancode
RUN pip install execnet
RUN git clone https://github.com/nexB/scancode-toolkit.git
RUN cd scancode-toolkit && \
    git checkout -b test_scancli 96069fd84066c97549d54f66bd2fe8c7813c6b52

# Dealing with utils.py
WORKDIR /home/runner/work/grimoirelab-graal/grimoirelab-graal/
RUN ln -s /graal/exec/ exec


RUN apt-get clean
WORKDIR /graal/
COPY ./ /graal/

RUN pip install --upgrade pip
RUN pip install -r "requirements.txt"

# Dependencies for testing
RUN pip install coveralls
RUN gem install github-linguist -v 7.12.2

RUN ./setup.py install
