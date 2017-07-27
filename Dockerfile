FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04
MAINTAINER Sergi Valverde <svalverde@eia.udg.edu>

# Install git, wget, python-dev, pip, BLAS + LAPACK and other dependencies
RUN apt-get update && apt-get install -y \
  gfortran \
  git \
  wget \
  liblapack-dev \
  libopenblas-dev \
  python-dev \
  python-pip \
  python-nose \
  python-numpy \
  python-scipy

# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin

USER root

# CNN necessary files 
ADD .theanorc /root/.theanorc
ADD ROBEX /ROBEX 
ADD WMH_challenge /src
ADD preprocess.py /preprocess.py
ADD test_net.py /test_net.py
ADD CASC_25_3D_256_128_64 /CASC_25_3D_256_128_64

# install packages
RUN pip install pip --upgrade
RUN pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
RUN pip install -r /src/requirements.txt




