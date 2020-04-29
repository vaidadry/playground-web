from datetime import datetime
from views import db


class FoodMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String, nullable=False, unique=True)
    comfortfood = db.Column(db.Boolean)
    fish = db.Column(db.Boolean)
    meal = db.Column(db.String, nullable=False)
    recipe = db.Column(db.String, nullable=False, unique=True)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow) # logs the datetime when email was sent(not when pushed in DB)
    email = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<New message on web: from: {self.email}, about: {self.subject}, message: {self.message}>"