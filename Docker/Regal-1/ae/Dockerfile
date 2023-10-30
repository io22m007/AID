FROM debian:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip unzip git avahi-utils
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN pip3 install RPi.GPIO
RUN pip3 install requests
RUN pip3 install 'git+https://github.com/gandalf15/HX711.git#egg=HX711&subdirectory=HX711_Python3'
CMD ls -la
CMD python3 AE_Application.py
