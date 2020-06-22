import wisdomgenerator

import secretsauce
from twilio.rest import Client

account_sid = secretsauce.ACCOUNT_SID
auth_token = secretsauce.AUTH_TOKEN
client = Client(account_sid, auth_token)



wisdomgenerator.send(client)