from database import db
from flask_login import UserMixin

class Meal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(80))
  hour = db.Column(db.DateTime)
  is_it_on_diet = db.Column(db.Boolean, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 