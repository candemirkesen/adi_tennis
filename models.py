from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
 
db = SQLAlchemy()

class TennisScores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(20))
    score = db.Column(db.Integer)