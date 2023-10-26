# Raspberry Pi Setup
## Raspberry Pi OS Config:
- hostname: `acme-in` (everyone needs this one), `acme-regal-1` (already one) or `acme-regal-2` (none so far)
- enable ssh with password
- username `acme`
- password `acme`
- setup your Wifi (don't forget the WiFi country)
- setting the keyboard language to de is usefull if you would need to connect a keyboard via USB

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
### git commands
get latest version update from GitHub:
```
git pull
```
add a file to git:
```
git add <filepath>
```
prepare for upload (an editor will open, add commit message at the bottom of the file):
```
git commit -a
```
upload to GitHub
```
git push
```
### to run acme on bare metal
This command in the acme folder:
```
sudo apt install pyhton3-pip  pyhton3-venv
```
```
python3 -m venv .
```
Then install requirements:
```
./bin/pip3 install -r requirements.txt
```

### docker
```
sudo apt install docker.io docker-compose
```
```
sudo usermod -aG docker $USER
```
```
sudo systemctl enable --now docker
```
```
sudo shutdown -r now
```