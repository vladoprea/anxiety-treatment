from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, flash, request, url_for, session
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
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

#Journal Entry Class
class JournalForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=100)])
    body = TextAreaField('Description', [validators.Length(min=30)])

#TFB Cycle Entry Class
class ToughtsForm(Form):
    situation = StringField('Situation', [validators.Length(min=15)])
    feeling = StringField('Feeling', [validators.Length(min=5)])
    rate_feeling = SelectField(u'Rate Feeling', choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    physical = StringField('Physical Reaction', [validators.Length(min=15)])
    behaviour = StringField('Behaviours', [validators.Length(min=15)])
    hot_tought = StringField('Hot Tought', [validators.Length(min=5)])
    evidence = TextAreaField('Evidence that support the hot tought', [validators.Length(min=30)])
    counter_evidence = TextAreaField('Counter Evidence for the hot tought', [validators.Length(min=30)])
    alternative = TextAreaField('Alternative/Balanced toughts', [validators.Length(min=30)])


@app.route('/')
def home():
    if 'email' in session:
        return render_template('dashboard.html', name=session['email'])
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html', name=session['email'])
    return render_template('dashboard.html')


@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')


@app.route('/treatment')
def treatment():
    return render_template('treatment.html')


@app.route('/journal')
def journal():
    return render_template('journal.html', journals=mongo.db.journals.find())


@app.route('/add_journal')
def add_journal():
    form = JournalForm()
    return render_template('add_journal.html', form=form)

@app.route('/insert_journal', methods=['POST'])
def insert_journal():
    form = JournalForm(request.form)
    journals = mongo.db.journals

    if request.method == 'POST' and form.validate():
        journals.insert_one(request.form.to_dict())
        return redirect(url_for('journal'))

    return redirect(url_for('add_journal'))


@app.route('/tfb_cycle')
def tfb_cycle():
    return render_template('tfb_cycle.html', toughts=mongo.db.toughts.find())


@app.route('/add_tought')
def add_tought():
    form =ToughtsForm()
    return render_template('add_tought.html', form=form)


@app.route('/insert_tought', methods=['POST'])
def insert_tought():
    form = ToughtsForm(request.form)
    toughts = mongo.db.toughts

    if request.method == 'POST' and form.validate():
        toughts.insert_one(request.form.to_dict())
        return redirect(url_for('tfb_cycle'))

    return redirect(url_for('add_tought'))


@app.route('/edit_journal/<journal_id>')
def edit_journal(journal_id):
    form = JournalForm()
    new_journal = mongo.db.journals.find_one({"_id": ObjectId(journal_id)})
    return render_template('edit_journal.html', form = form, journal = new_journal)

@app.route('/update_journal/<journal_id>', methods=["GET", "POST"])
def update_journal(journal_id):
    journals = mongo.db.journals
    journals.update( {'_id': ObjectId(journal_id)},
    {
        'title': request.form.get('title'),
        'body': request.form.get('body')
    })
    return redirect(url_for('journal'))


@app.route('/edit_tought/<tought_id>')
def edit_tought(tought_id):
    form = ToughtsForm()
    new_tought = mongo.db.toughts.find_one({"_id": ObjectId(tought_id)})
    return render_template('edit_tought.html', form = form, tought = new_tought)

@app.route('/update_tought/<tought_id>', methods=["POST"])
def update_tought(tought_id):
    toughts = mongo.db.toughts
    toughts.update( {'_id': ObjectId(tought_id)},
    {
        'situation': request.form.get('situation'),
        'feeling': request.form.get('feeling'),
        'rate_feeling': request.form.get('rate_feeling'),
        'physical': request.form.get('physical'),
        'behaviour': request.form.get('behaviour'),
        'evidence': request.form.get('evidence'),
        'counter_evidence': request.form.get('counter_evidence'),
        'alternative': request.form.get('alternative')

    })
    return redirect(url_for('tfb_cycle'))


@app.route('/delete_journal/<journal_id>')
def delete_journal(journal_id):
    mongo.db.journals.remove({'_id': ObjectId(journal_id)})
    return redirect(url_for('journal'))


@app.route('/delete_tought/<tought_id>')
def delete_tought(tought_id):
    mongo.db.toughts.remove({'_id': ObjectId(tought_id)})
    return redirect(url_for('tfb_cycle'))


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
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        users = mongo.db.users
        email_login = users.find_one({'email': request.form['email']})

        if email_login:
            if check_password_hash(email_login['password'], request.form["password"]):
                session['email'] = request.form['email']
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))
        
        flash('Username does not exist')
        return redirect(url_for('register'))
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """ clears session logging the user out """
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=False)
