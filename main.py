from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask import session
from sqlalchemy.sql import text
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pymysql

# import mysql.connector

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123456",
#     database="tennis_scores"
# )

# my_cursor = mydb.cursor()

# from flask import send_from_directory
# import json
# from models import TennisScores, db

# from google.cloud.sql.connector import Connector, IPTypes

# Python Connector database connection function
# def getconn():
#     with Connector() as connector:
#         conn = connector.connect(
#             "scores-364816:europe-central2:adi-tennis-db", # Cloud SQL Instance Connection Name
#             "pymysql",
#             user="root",
#             password="",
#             db="adi-tennis-db",
#             ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
#         )
#         return conn

# Google Cloud SQL (change this accordingly)
PASSWORD =''
PUBLIC_IP_ADDRESS ='34.118.109.6'
DBNAME ='score_table'
PROJECT_ID ='scores-364816'
INSTANCE_NAME ='tennis-367213:europe-central2:tennisdb'

# mydb = mysql.connector.connect(
#     host="34.118.20.170",
#     user="root",
#     password="",
#     database="score_table"
# )


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adi_tennis.db'
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@{PUBLIC_IP_ADDRESS}/{DBNAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@/cloudsql/{INSTANCE_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+pymysql://root:123456@/score_table?unix_socket=/cloudsql/tennis-367213:europe-central2:tennisdb'
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@localhost/tennis_scores"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql://root:123456@localhost/tennis_scores"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# /cloudsql/{your-cloudsql-connection-string}

# engine = create_engine('mysql://root:123456@localhost/tennis_scores')

db = SQLAlchemy(app)
db.app = app

class scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(20))
    score = db.Column(db.Integer)

    def __repr__(self):
        return self.player
        return '<Player %r>' % self.player

# @app.before_first_request
# def create_table():
#     db.create_all()

# df = pd.read_csv('scores.csv')

def updateScores_db(r_a, r_b): #r_a and r_b previous scores a and b. a is winner, b is loser
  s_a = 1 # means a is winner
  s_b = 0 # means b is loser
  temp_var = (r_b - r_a) / 400
  e_a = 1 / (1 + pow(10, temp_var))
  e_b = 1 / (1 + pow(10, -temp_var))
  return round(r_a + 20*(s_a-e_a)), round(r_b + 20*(s_b-e_b))


@app.route("/", methods=["GET", "POST"])
def home():

    # if selection is None:
    winner = 'anan'
    loser = 'anan'
    players = scores.query.order_by(scores.score.desc())
    champion = scores.query.order_by(scores.score.desc()).first()
    # my_cursor.execute("SELECT * FROM scores")

    if request.method == 'POST':
        winner = request.form['winner']
        loser = request.form['loser']

        if winner == loser:
            pass
        else:
            winner_player = scores.query.filter_by(player=winner).first()
            loser_player = scores.query.filter_by(player=loser).first()
            winner_player.score, loser_player.score = updateScores_db(winner_player.score, loser_player.score)
            db.session.commit()

    champion = scores.query.order_by(scores.score.desc()).first()
    return render_template("homepage.html", winner=winner, loser=loser, champion=champion, players=players)


if __name__ == '__main__':
	app.run(debug=False)
