# Advanced IoT Systems Development
## Raspberry Pi Pinout:
![](Pinout.png)
## Raspberry Pi OS Config:
- hostname: `acme-in` (everyone needs this one), `acme-regal-1` (already one) or `acme-regal-2` (none so far)
- enable ssh with password
- username `acme`
- password `acme`
- setup your WiFi (don't forget the WiFi country)
- SSID: `150PowerToGo`
- passwort `htmt4954`
- setting the keyboard language to `de` is usefull if you need to connect a keyboard via USB

## Install on Pi:
### gerneral apt packages
```
sudo apt update
```
```
sudo apt upgrade
```
```
sudo apt install git
```
### clone git
- Create Troken for your git account: https://github.com/settings/tokens (give the token a name, set an expiration date and select the scope "repo")
- Clone with this command (replace <your_token> with your new token):
```
git clone https://<your_token>@github.com/io22m007/AID
```
tell git that the directory is a save directory
```
git config --global --add safe.directory /home/acme/AID
```
### docker
install docker:
```
sudo apt install docker.io docker-compose
```
add current user to docker group:
```
sudo usermod -aG docker $USER
```
enable docker at startup:
```
sudo systemctl enable --now docker
```
restart system:
```
sudo shutdown -r now
```
### calibrate scale
To calibrate the scale you need to run the `scale-calibrate.py` Python app.

This app can be found in the `Tools` folder.

You'll need an object of which you know the exact weight.

Follow the instructions in the Python app and copy the config string into the `ae.ini` file. This file can be found here:
- /AID/Docker/Regal-1/ae/ae.ini
- /AID/Docker/Regal-2/ae/ae.ini

### run docker container
switch to one of these folders:
- /AID/Docker/Infra
- /AID/Docker/Regal-1
- /AID/Docker/Regal-2
start docker container:
```
docker-compose up --build
```
start docker container in the background:
```
docker-compose up --build -d
```
## Helpful commands:
[a list of helpful commands can be found here](Command-Help.md)