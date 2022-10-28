from flask import Flask, render_template, request, redirect, url_for
# from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
# from flask import session
# from sqlalchemy.sql import text
import sqlalchemy
import os
# from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# from sqlalchemy import inspect
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
PASSWORD ='123456'
PUBLIC_IP_ADDRESS ='34.118.20.170' # 34.118.20.170  34.159.140.186
DBNAME ='score_table'
PROJECT_ID ='scores-364816'
INSTANCE_NAME ='scores-364816:europe-west3:mycloudsql'


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
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@{PUBLIC_IP_ADDRESS}/{DBNAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@{INSTANCE_NAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://root:123456@localhost/tennis_scores"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql://root:123456@localhost/tennis_scores"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@score_table?unix_socket=/cloudsql/scores-364816:europe-central2:adi-tennis-db'

engine = sqlalchemy.create_engine("mysql+pymysql://root:123456@34.159.140.186/score_table")
# engine = sqlalchemy.create_engine("mysql+pymysql://root:123456@34.118.20.170/cloudsql/scores-364816:europe-central2:adi-tennis-db")

app.config['SQLALCHEMY_DATABASE_URI'] = engine.url.render_as_string(hide_password=False)


# engine = create_engine('mysql://root:123456@localhost/tennis_scores')

# with engine.connect() as con:
#     rs = con.execute('SELECT * FROM scores')
#     for row in rs:
#         print('ananananan')
#         print(row)

# print(rs)    
# for row in rs:
#     print('ananananan')
#     print(row)

# configure Flask-SQLAlchemy to use Python Connector
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql + mysqldb://"
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     "creator": getconn
# }


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

def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_user = 'root' #os.environ["root"]  # e.g. 'my-database-user'
    db_pass = '123456' # os.environ["123456"]  # e.g. 'my-database-password'
    db_name = 'score_table' #os.environ["score_table"]  # e.g. 'my-database'
    unix_socket_path = '/cloudsql/scores-364816:europe-central2:adi-tennis-db' # os.environ["/cloudsql/scores-364816:europe-central2:adi-tennis-db"]  # e.g. '/cloudsql/project:region:instance'

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": unix_socket_path},
        ),
        # ...
    )
    return pool

# pool = connect_unix_socket()
# print(f"pool is : {pool}")
# pool.connect()


@app.route("/", methods=["GET", "POST"])
def home():

    # connect_unix_socket()

    # if selection is None:
    winner = 'anan'
    loser = 'anan'
    players = scores.query.order_by(scores.score.desc())
    # print(players)
    # champion = scores.query.filter_by(player=loser).first()
    champion = 'anan'
    # my_cursor.execute("SELECT * FROM scores")


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


        # with engine.connect() as con:
        #     rs = con.execute('SELECT * FROM scores')

        # print(rs)    
        # for row in rs:
        #     print('ananananan')
        #     print(row)

        # players = scores.query.order_by(scores.score)
        # print(f'players: {players}')

        # new_game = TennisScores(player=winner, score=1111)
        # db.session.add(new_game)
        # db.session.commit()


    # idx = df['Score'].idxmax()
    # champion = df.Player[idx]
    # return f'Result: {players}'
    return render_template("homepage.html", winner=winner, loser=loser, champion=champion, players=players)


if __name__ == '__main__':
	app.run(debug=False)
