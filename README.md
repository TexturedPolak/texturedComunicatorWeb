# TexturedComunicator
![GitHub](https://img.shields.io/github/license/TexturedPolak/texturedComunicatorWeb)
![GitHub Repo stars](https://img.shields.io/github/stars/TexturedPolak/texturedComunicatorWeb)
![GitHub issues](https://img.shields.io/github/issues/TexturedPolak/texturedComunicatorWeb)

## About
That's simple (very simple) comunicator to send text messages. It's writen in python and using Bottle library.<br> TexturedComunicator have hosted instance on <a href="https://chat.texturedpolak.xyz">https://chat.texturedpolak.xyz</a> .
## Hosted instance details
Hosted instance is protected with end-to-end TLS encryption and is protected with Cloudflare.
## API reference
## USE API WITH MIND on hosted instance
### URL
For all requests is one URL:
* for hosted instance: <a href="https://chat.texturedpolak.xyz/api">https://chat.texturedpolak.xyz/api</a>
* for self-hosted: your_ip_or_domain/api
### Check new messages
METHOD: **POST**<br>
Content Type: **application/x-www-form-urlencoded**<br>
Payload: ```{id: your_last_message_id (int)}```<br>
Response: ```{reload: true/false}```
### Get new messages (not use for checking new messages, pls)
METHOD: **PATCH**<br>
Content Type: **application/json**<br>
Payload: ```{lastId: your_last_message_id(int or str), passwordHash: your_password_hash(str), username: your_username(str)}``` <br>
Response: ```{id: latest_message_id(int), messages: all_new_messages(str)}```
### Send message
METHOD: **PUT**<br>
Content Type: **application/json**<br>
Payload: ```{message: message_to_send(str), passwordHash: your_password_hash (str), username: your_username (str)}``` <br>
Response: No Response, only Status Code
