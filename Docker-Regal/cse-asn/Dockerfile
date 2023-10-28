FROM debian:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip unzip wget avahi-utils
RUN wget https://github.com/ankraft/ACME-oneM2M-CSE/archive/refs/tags/0.12.0.zip
RUN unzip 0.12.0.zip -d ACME-oneM2M-CSE
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN pip3 install -v -r ACME-oneM2M-CSE/ACME-oneM2M-CSE-0.12.0/requirements.txt
CMD cd ACME-oneM2M-CSE/ACME-oneM2M-CSE-0.12.0 && python3 -m acme
