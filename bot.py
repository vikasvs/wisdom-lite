from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import sys
import logging
import random 
import secretsauce

app = Flask(__name__)

bank = secretsauce.bank
quoteBank = secretsauce.quoteBank
thoughts = secretsauce.thoughts
userBank = []


@app.route('/bot2', methods=['GET', 'POST'])
def bot2():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_nmbr = request.values.get('From')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    #models.User.query.delete()

    if "recruiting" in incoming_msg:
        msg.body('https://www.notion.so/vikassharma/Recruiting-Guide-fcdbbe5eb9f3417ab68349df03740294')
        responded = True
    elif "subscribe" in incoming_msg:
        userBank.append(incoming_nmbr)
        msg.body(random.choice(quoteBank))
        responded = True
    elif 'im cooking' in incoming_msg:
        msg.body("are you sure: respond yes if so")
        responded = True
    elif 'yes' in incoming_msg:
        userBank.append('incoming_nmbr')
        msg.body(random.choice(bank))
        responded = True
    elif 'thoughts' in incoming_msg:
        userBank.append('incoming_nmbr')
        msg.body(random.choice(thoughts))
        responded = True
    elif 'ventures' in incoming_msg:
        msg.body('https://proverify.herokuapp.com/')
        responded = True
    if not responded:
        msg.body('Hi wisdom-lite offers a few features, to get information about recruiting, text "recruiting", to learn about ventures, text "ventures", to get life advice from time-tested books, thoughts for my thoughts, and relevant innovators text "subscribe", and if youre particularly risky, text " im cooking". Enjoy')
    return str(resp)

if __name__ == "__main__":
    app.run()



