from __init__ import db, _update_db
import random
from datetime import datetime, timezone
from presets import roastBank, quoteBank, excuseBank, complimentBank


class User(db.Model):
    __tablename__ = "users"

    phone_number = db.Column(db.Text, primary_key=True)
    
    creating_flashcards = db.Column(db.Boolean, default=False)
    add_insult_flag = db.Column(db.Boolean, default=False)
    add_quote_flag = db.Column(db.Boolean, default=False)
    add_excuse_flag = db.Column(db.Boolean, default=False)
    add_compliment_flag = db.Column(db.Boolean, default=False)
    add_recurring_flag = db.Column(db.Boolean, default=False)
    
    # Relationship to saved items
    saved_items = db.relationship('SavedItem', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.add_insult_flag = False
        self.add_quote_flag = False
        self.add_excuse_flag = False
        self.add_compliment_flag = False
        self.add_recurring_flag = False

    def load(self):
        """Load preset content into user's saved items"""
        for r in roastBank:
            self._add_item('roast', r)
        for q in quoteBank:
            self._add_item('quote', q)
        for e in excuseBank:
            self._add_item('excuse', e)
        for c in complimentBank:
            self._add_item('compliment', c)
        _update_db(self)
        return True

    def _add_item(self, kind, text):
        """Internal method to add a saved item"""
        item = SavedItem(user_id=self.phone_number, kind=kind, text=text)
        db.session.add(item)

    def _get_items(self, kind):
        """Internal method to get all items of a specific kind"""
        return [item.text for item in self.saved_items if item.kind == kind]

    def _get_random_item(self, kind):
        """Internal method to get a random item of a specific kind"""
        items = self._get_items(kind)
        if not items:
            return None
        return random.choice(items)

    def _remove_item(self, kind, text):
        """Internal method to remove a saved item"""
        item = SavedItem.query.filter_by(
            user_id=self.phone_number, 
            kind=kind, 
            text=text
        ).first()
        if item:
            db.session.delete(item)
            _update_db(self)
            return "removed"
        return None

    # Roasts
    def add_roast(self, msg):
        self._add_item('roast', msg)
        return True

    def get_roast(self):
        return self._get_random_item('roast')

    def remove_insult(self, msg):
        return self._remove_item('roast', msg)

    # Quotes
    def add_quote(self, msg):
        self._add_item('quote', msg)
        return True

    def get_quote(self):
        return self._get_random_item('quote')

    def remove_quote(self, msg):
        return self._remove_item('quote', msg)

    # Compliments
    def add_compliment(self, msg):
        self._add_item('compliment', msg)
        return True

    def get_compliment(self):
        return self._get_random_item('compliment')

    def remove_compliment(self, msg):
        return self._remove_item('compliment', msg)

    # Excuses
    def add_excuse(self, msg):
        self._add_item('excuse', msg)
        return True

    def get_excuse(self):
        return self._get_random_item('excuse')

    def remove_excuse(self, msg):
        return self._remove_item('excuse', msg)

    # Recurring
    def add_recurring(self, msg):
        self._add_item('recurring', msg)
        return True

    def get_recurring(self):
        return self._get_random_item('recurring')

    def remove_recurring(self, msg):
        return self._remove_item('recurring', msg)


class SavedItem(db.Model):
    __tablename__ = "saved_items"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.phone_number'), nullable=False)
    kind = db.Column(db.String(50), nullable=False)  # 'roast', 'quote', 'excuse', 'compliment', 'recurring'
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship back to user
    user = db.relationship('User', back_populates='saved_items')
    
    def __repr__(self):
        return f'<SavedItem {self.kind}: {self.text[:30]}...>'
