## git commands
get latest version update from GitHub:
```
git pull
```
Resolve `pulling without specifying how to reconcile divergent branches is discouraged` issue:
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
view status of git:
```
git status
```
prepare for upload (replace the word message with a commit message):
```
git commit -a -m "message"
```
upload to GitHub
```
git push
```
roll back file
```
git restore filepath
```
## certificates
edit `/etc/ssl/openssl.cnf` file:
* in region `[ req_distinguished_name ]`
  - countryName_default: AT
  - stateOrProvinceName_default: Vienna
  - 0.organizationName_default: MIO-3
  - commonName_default (new): CA

create root certificate authority (passphrase for key will be `acme`, everything else defaults):
```
/usr/lib/ssl/misc/CA.pl -newca
```
new root certificate authority certificate will be in `./demoCA/cacert.pem` and root certificate authority private key will be in `./demoCA/private/cakey.pem`

verify certificate details:
```
openssl x509 -in demoCA/cacert.pem -text -noout
```
create a key:
```
openssl genrsa -out server.key 2048
```
create a certificate request:
```
openssl req -new -out server.csr -key server.key -subj "/C=AT/ST=Vienna/L=/O=MIO-3/OU=/CN=hostname.local"
```
from the certificate request create a certificate signed by the root certificate authority using a configfile for the subjectAltName:
```
openssl ca -in server.csr -out server.crt -extfile subjectAltName.conf
```
this is an example configfile for the subjectAltName
```
basicConstraints=CA:FALSE
subjectAltName=@my_subject_alt_names
subjectKeyIdentifier = hash

[ my_subject_alt_names ]
DNS.1 = hostname.local
DNS.2 = hostname
```
## create symbolic link example
target -> symbolic link file location

if paths are relative then you need to account for each step
```
ln -s ../../../CA/ demoCA
```