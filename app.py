from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
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
login_manager = LoginManager(app)


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
    body = TextAreaField('Description')

#TFB Cycle Entry Class
class ToughtsForm(Form):
    situation = StringField('Situation', [validators.Length(min=5)])
    feeling = StringField('Feeling')
    rate_feeling = SelectField(u'Rate Feeling', choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    physical = StringField('Physical Reaction')
    behaviour = StringField('Behaviours')
    hot_tought = StringField('Hot Tought')
    evidence = TextAreaField('Evidence that support the hot tought')
    counter_evidence = TextAreaField('Counter Evidence for the hot tought')
    alternative = TextAreaField('Alternative/Balanced toughts')

class User:

    def __init__(self, email):
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

@login_manager.user_loader
def load_user(email):
    users = mongo.db.users
    u = users.find_one({'email': email})
    if not u:
        return None
    return User(email=u['email'])


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')


@app.route('/treatment')
def treatment():
    return render_template('treatment.html')


@app.route('/help_guide')
def help_guide():
    return render_template('help_guide.html')


@app.route('/journal')
@login_required
def journal():

    return render_template('journal.html', journals=mongo.db.journals.find())


@app.route('/add_journal')
@login_required
def add_journal():
    form = JournalForm()
    return render_template('add_journal.html', form=form)

@app.route('/insert_journal', methods=['POST'])
@login_required
def insert_journal():
    form = JournalForm(request.form)
    journals = mongo.db.journals
    new_journal = request.form.to_dict()
    new_journal['owner']=session['email']
    print(new_journal)

    if request.method == 'POST' and form.validate():
        journals.insert_one(new_journal)
        return redirect(url_for('journal'))

    return redirect(url_for('add_journal'))


@app.route('/tfb_cycle')
@login_required
def tfb_cycle():
    return render_template('tfb_cycle.html', toughts=mongo.db.toughts.find())


@app.route('/add_tought')
@login_required
def add_tought():
    form =ToughtsForm()
    return render_template('add_tought.html', form=form)


@app.route('/insert_tought', methods=['POST'])
@login_required
def insert_tought():
    form = ToughtsForm(request.form)
    toughts = mongo.db.toughts

    if request.method == 'POST' and form.validate():
        toughts.insert_one(request.form.to_dict())
        return redirect(url_for('tfb_cycle'))

    return redirect(url_for('add_tought'))


@app.route('/edit_journal/<journal_id>')
@login_required
def edit_journal(journal_id):
    new_journal = mongo.db.journals.find_one({"_id": ObjectId(journal_id)})
    form = JournalForm()
    print(new_journal)
    return render_template('edit_journal.html', form = form, journal = new_journal)

@app.route('/update_journal/<journal_id>', methods=["GET", "POST"])
@login_required
def update_journal(journal_id):
    journals = mongo.db.journals
    journals.update( {'_id': ObjectId(journal_id)},
    {
        'title': request.form.get('title'),
        'body': request.form.get('body')
    })
    return redirect(url_for('journal'))


@app.route('/edit_tought/<tought_id>')
@login_required
def edit_tought(tought_id):
    new_tought = mongo.db.toughts.find_one({"_id": ObjectId(tought_id)})
    form = ToughtsForm()
    print(new_tought)
    return render_template('edit_tought.html', form = form, tought = new_tought)

@app.route('/update_tought/<tought_id>', methods=["POST"])
@login_required
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
        user_login = users.find_one({'email': request.form['email']})

        if user_login and User.validate_login(user_login['password'], request.form["password"]):
            user_obj = User(email=user_login['email'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        
        flash('Username does not exist')
        return redirect(url_for('register'))
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=False)
