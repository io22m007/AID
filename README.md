# Advanced IoT Systems Development
## Raspberry Pi OS Config:
- hostname: `acme-in` (everyone needs this one), `acme-regal-1` (already one) or `acme-regal-2` (none so far)
- enable ssh with password
- username `acme`
- password `acme`
- setup your Wifi (don't forget the WiFi country)
- SSID: `150PowerToGo`
- passwort `htmt4954`
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
### tell git that the directory is a save directory
```
git config --global --add safe.directory /home/acme/AID
```
### git commands
get latest version update from GitHub:
```
git pull
```
### Resolve `pulling without specifying how to reconcile divergent branches is discouraged` issue:
```
git config pull.rebase false
```
configure git account for upload:
```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
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
start docker container:
```
docker-compose up --build
```
start docker container in the background:
```
docker-compose up --build -d
```
### certificates
root certificate authority key (passphrase will be `acme`):
```
openssl genrsa -des3 -out ca.key 2048
```
root certificate authority (with Country Name `AT`, State `Vienna` and Organization Name `MIO-3`):
```
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt
```
create a key:
```
openssl genrsa -out server.key 2048
```
create a certificate request:
```
openssl req -new -out server.csr -key server.key -addext "subjectAltName = DNS:hostname.local" -subj "/C=AT/ST=Vienna/L=/O=MIO-3/OU=/CN=hostname.local"
```
from the certificate request create a certificate signed by the root certificate authority:
```
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650
```
