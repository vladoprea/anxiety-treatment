from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, flash, request, url_for, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
import os
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

# Register From Class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

#Login Form Class
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])


@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', name=session['username'])
    return render_template('home.html')




@app.route('/symptoms')
def sym():
    return render_template('symptoms.html')


@app.route('/treatment')
def treat():
    return render_template('treatment.html')

#User Register
@app.route('/register' , methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        users = mongo.db.users
        user_exist = users.find_one({'username' : request.form['username']})
        email_exist = users.find_one({'email': request.form['email']})

        if user_exist is None:
            if email_exist is None:
                hashpass = generate_password_hash(request.form["password"])
                users.insert({'username' : request.form['username'], 'email': request.form['email'] , 'password' : hashpass})
                session['username'] = request.form['username']
                return redirect(url_for('login'))
            
            flash('That email already exists')
            return redirect(url_for('register'))
        
        flash('That username already exists!')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)

#User Login
@app.route('/login' , methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        users = mongo.db.users
        user_login = users.find_one({'username': request.form['username']})

        if user_login:
            if check_password_hash(user_login['password'], request.form["password"]):
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))
        
        flash('Username does not exist')
        return redirect(url_for('register'))
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """ clears session logging the user out """
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=False)
