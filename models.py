from __init__ import db, _update_db
import random
from secretsauce import *

class User(db.Model):
    __tablename__ = "users"

    phone_number = db.Column(db.Text, primary_key=True)

    recurring = []
    roasts = []
    quotes = []
    excuses = []
    compliments = []
    
    creating_flashcards = db.Column(db.Boolean)
    add_insult_flag = db.Column(db.Boolean)
    add_quote_flag = db.Column(db.Boolean)
    add_excuse_flag = db.Column(db.Boolean)
    add_compliment_flag = db.Column(db.Boolean)
    add_recurring_flag = db.Column(db.Boolean)


    def __init__(self, phone_number):
        self.phone_number = phone_number

        self.add_insult_flag = False
        self.add_quote_flag = False
        self.add_excuse_flag = False
        self.add_compliment_flag = False
        self.add_recurring_flag = False

        quotes = []
        roasts = []
        excuses = []
        compliments = []
        recurring = []


    def load(self):
        for r in roastBank:
            self.roasts.append(r)
        for q in quoteBank:
            self.quotes.append(q)
        for e in excuseBank:
            self.excuses.append(e)
        for c in complimentBank:
            self.compliments.append(c)
        _update_db(self)
        return True

    #roasts
    def add_roast(self, msg):
        self.roasts.append(msg)
        return True

    def get_roast(self):
        if self.roasts is None:
            return None
        else:
            insult = random.choice(self.roasts)
            _update_db(self)
        return insult

    def remove_insult(self, msg):
        if self.roasts is None:
            return None
        else:
            self.roasts.remove(msg)
            _update_db(self)
        return "removed"

    #quotes
    def add_quote(self, msg):
        self.quotes.append(msg)
        return True

    def get_quote(self):
        if self.quotes is None:
            return None
        else:
            qt = random.choice(self.quotes)
            _update_db(self)
        return qt

    def remove_quote(self, msg):
        if self.quotes is None:
            return None
        else:
            self.quotes.remove(msg)
            _update_db(self)
        return "removed"

    #compliments
    def add_compliment(self, msg):
        self.compliments.append(msg)
        return True

    def get_compliment(self):
        if self.compliments is None:
            return None
        else:
            compliment = random.choice(self.compliments)
            _update_db(self)
        return compliment

    def remove_compliment(self, msg):
        if self.compliments is None:
            return None
        else:
            self.compliments.remove(msg)
            _update_db(self)
        return "removed"

    #excuses
    def add_excuse(self, msg):
        self.excuses.append(msg)
        return True
    def get_excuse(self):
        if self.excuses is None:
            return None
        else:
            excuse = random.choice(self.excuses)
            _update_db(self)
        return excuse

    def remove_excuse(self, msg):
        if self.excuses is None:
            return None
        else:
            self.excuses.remove(msg)
            _update_db(self)
        return "removed"


    #recurring
    def add_recurring(self, msg):
        self.recurring.append(msg)
        return True

    def get_recurring(self):
        if self.recurring is None:
            return None
        else:
            r = random.choice(self.recurring)
            _update_db(self)
        return r

    def remove_recurring(self, msg):
        if self.recurring is None:
            return None
        else:
            self.recurring.remove(msg)
            _update_db(self)
        return "removed"
