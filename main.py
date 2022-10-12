from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms import RadioField
from wtforms.validators import DataRequired
import pandas as pd
import os
# from random import sample
from random import randint
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user # After authentication
from flask_login import login_required
from flask_login import logout_user
from werkzeug.utils import secure_filename
from flask import session
from flask import send_from_directory
import json

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"

df = pd.read_csv('scores.csv')


@app.route("/", methods=["GET", "POST"])
def home():
    # image_path = getWinnerFullPath(session['df'])
    # return render_template("homepage.html", dframe=df, n=len(df), winner_path=image_path)
    return render_template("homepage.html", dframe=df, n=len(df))



if __name__ == '__main__':
	app.run(debug=False)
