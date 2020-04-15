from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, flash, request, url_for
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import os
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/symptoms.html')
def sym():
    return render_template('symptoms.html')


@app.route('/treatment.html')
def treat():
    return render_template('treatment.html')

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=False)
