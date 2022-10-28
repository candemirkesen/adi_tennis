from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, DateField
# from wtforms import RadioField
from wtforms.validators import DataRequired
# import pandas as pd
# import os
# from random import sample
# from random import randint
from flask_sqlalchemy import SQLAlchemy
# from flask_login import current_user, login_user # After authentication
# from flask_login import login_required
# from flask_login import logout_user
# from werkzeug.utils import secure_filename
from flask import session
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
# PASSWORD =''
# PUBLIC_IP_ADDRESS ='34.118.20.170'
# DBNAME ='adi-tennis-db'
# PROJECT_ID ='scores-364816'
# INSTANCE_NAME ='scores-364816:europe-central2:adi-tennis-db'

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adi_tennis.db'
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@localhost/tennis_scores"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql://root:123456@localhost/tennis_scores"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configure Flask-SQLAlchemy to use Python Connector
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql + mysqldb://"
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     "creator": getconn
# }


db = SQLAlchemy(app)
# db.app = app

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
    players = scores.query.order_by(scores.score)
    champion = scores.query.filter_by(player=loser).first()


    # for i in range(len(df)):
    #     player_name = df.Player[i]
    #     player_score = df.Score[i]
    #     new_game = TennisScores(player=player_name, score=int(player_score))
    #     db.session.add(new_game)
    #     db.session.commit()
    # db.session.commit()

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


        players = scores.query.order_by(scores.score)

        # new_game = TennisScores(player=winner, score=1111)
        # db.session.add(new_game)
        # db.session.commit()


    # idx = df['Score'].idxmax()
    # champion = df.Player[idx]
    print(f'players: {players}')
    return render_template("homepage.html", winner=winner, loser=loser, champion=champion, players=players)



if __name__ == '__main__':
	app.run(debug=False)
