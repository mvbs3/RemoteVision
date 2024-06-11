# RemoteVision

## Front end

To start react server:
` npm start`

### To start react as HTTPS:

Windowns
` set HTTPS=true&&npm start`
Windowns power shell
` ($env:HTTPS = "true") -and (npm start)`
Linux/MacOS
` HTTPS=true npm start`

### Criar chave SSH

`openssl genpkey -algorithm RSA -out key.pem -aes256`

`openssl req -new -x509 -key key.pem -out cert.pem -days 365 `

### criar venv

`python3 -m venv venv`

#### entrar venv windowns

`.\venv\Scripts\activate`

#### entrar venv linux

`source venv/bin/activate`


`ssh -i ".../tcc-brasil-Server_key.pem" iang@20.197.224.24`
