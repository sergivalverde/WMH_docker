# --------------------------------------------------
# WMH challenge dockerfile 
#
# Sergi Valverde 2017
# --------------------------------------------------

FROM mcabezas/python_nolearn:ubuntu14.04-cudnn

MAINTAINER Sergi Valverde <svalverde@eia.udg.edu>

USER root

# We add all the necessary files to the image
ADD ROBEX /ROBEX 
ADD preprocess.py /preprocess.py
ADD test_net.py /test_net.py
ADD CASC_25_3D_256_128_64 /CASC_25_3D_256_128_64

# Configuration: load WMH challenge project and install requirements 
RUN git clone https://github.com/sergivalverde/WMH_challenge.git src
RUN pip install -r src/requirements.txt


# test_net infers WMH segmentation to the input passed as /INPUT/
CMD test_net.py
