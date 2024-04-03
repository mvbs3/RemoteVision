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
