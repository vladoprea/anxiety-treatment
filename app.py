from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for
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


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=False)
