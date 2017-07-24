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

# Configuration
RUN git clone https://github.com/sergivalverde/WMH_challenge.git src
RUN pip install nibabel

RUN cd /usr/local/nets/src && git submodule init && git submodule update --remote
RUN cd /usr/local/nets/src/cnn && git submodule init && git submodule update --remote
RUN cd /usr/local/nets/src && git submodule init && git submodule update --remote
RUN chmod 777 /bin/deep-challenge2016.sh

# We prepare it to run with the images
CMD deep-challenge2016.sh $@
