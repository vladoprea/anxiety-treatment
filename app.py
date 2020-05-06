from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, JournalForm, ToughtsForm
from flask_wtf.csrf import CSRFProtect
import datetime 
import os
from os import path
if path.exists("env.py"):
    import env


csrf = CSRFProtect()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

csrf.init_app(app)


# User class to implement these properties and methods, used in login:
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

# Callback used to reload the user object from the user email stored in the session
@login_manager.user_loader
def load_user(email):
    users = mongo.db.users
    u = users.find_one({'email': email})
    if not u:
        return None
    return User(email=u['email'])


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
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
    """
    Insert users input into database
    Checks if forms validate
    Add logged in user email to collection
    so that the inputs to be displayed for every user separately
    Add date and time of the post to database
    """
    form = JournalForm(request.form)
    journals = mongo.db.journals
    if form.validate_on_submit():
        if current_user.is_authenticated:
            journals.insert_one({
                'owner': current_user.email,
                'datetime': datetime.datetime.now().isoformat(' ', 'seconds'),
                'title': request.form.get('title'),
                'body': request.form.get('body')})
            flash('Your new experience was added to journal!', 'success')
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
    """
    Insert users input into database
    Checks if forms validate
    Add logged in user email to collection
    so that the inputs to be displayed for every user separately
    Add date and time of the post to database
    """
    form = ToughtsForm(request.form)
    toughts = mongo.db.toughts

    if form.validate_on_submit():
        if current_user.is_authenticated:
            toughts.insert_one({
                'owner': current_user.email,
                'datetime': datetime.datetime.now().isoformat(' ', 'seconds'),
                'situation': request.form.get('situation'),
                'feeling': request.form.get('feeling'),
                'rate_feeling': request.form.get('rate_feeling'),
                'physical': request.form.get('physical'),
                'behaviour': request.form.get('behaviour'),
                'hot_tought': request.form.get('hot_tought'),
                'evidence': request.form.get('evidence'),
                'counter_evidence': request.form.get('counter_evidence'),
                'alternative': request.form.get('alternative')})
            flash('Your new TFB cycle was added!', 'success')
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
    """
    Get the required post to be updated
    Update all fields besides 'owner' which it should be the same
    """
    journals = mongo.db.journals
    if current_user.is_authenticated:
        journals.update( {'_id': ObjectId(journal_id)},
        {   'owner': current_user.email,
            'datetime': datetime.datetime.now().isoformat(' ', 'seconds'),
            'title': request.form.get('title'),
            'body': request.form.get('body')
        })
        flash("Your selected entry was updated!", 'success')
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
    """
    Get the required post to be updated
    Update all fields besides 'owner' which it should be the same
    """
    toughts = mongo.db.toughts
    if current_user.is_authenticated:
        toughts.update( {'_id': ObjectId(tought_id)},
        {   
            'owner': current_user.email,
            'datetime': datetime.datetime.now().isoformat(' ', 'seconds'),
            'situation': request.form.get('situation'),
            'feeling': request.form.get('feeling'),
            'rate_feeling': request.form.get('rate_feeling'),
            'physical': request.form.get('physical'),
            'behaviour': request.form.get('behaviour'),
            'hot_tought': request.form.get('hot_tought'),
            'evidence': request.form.get('evidence'),
            'counter_evidence': request.form.get('counter_evidence'),
            'alternative': request.form.get('alternative')})
        flash('Your selected entry was updated!', 'success')
        return redirect(url_for('tfb_cycle'))

# Delete selected entry
@app.route('/delete_journal/<journal_id>')
def delete_journal(journal_id):
    mongo.db.journals.remove({'_id': ObjectId(journal_id)})
    return redirect(url_for('journal'))

# Delete selected entry
@app.route('/delete_tought/<tought_id>')
def delete_tought(tought_id):
    mongo.db.toughts.remove({'_id': ObjectId(tought_id)})
    return redirect(url_for('tfb_cycle'))


#User Register
@app.route('/register' , methods=['GET', 'POST'])
def register():
    """
    Check if the username and email already exists. 
    If yes, en error will be shown 
    If all validations pass, the password is hashed 
    then all details introduced to database
    """
    form = RegisterForm()
    if form.validate_on_submit():
        users = mongo.db.users
        user_exist = users.find_one({'username' : request.form['username']})
        email_exist = users.find_one({'email': request.form['email']})

        if user_exist is None:
            if email_exist is None:
                hashpass = generate_password_hash(request.form["password"])
                users.insert({'username': request.form['username'], 'email': request.form['email'] , 'password' : hashpass})
                flash('Your account was created!', 'success')
                return redirect(url_for('login'))
            
            flash('That email already exists', 'danger')
            return redirect(url_for('register'))
        
        flash('That username already exists!', 'danger')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login and validate the user. Check if the email exists in database 
    and if the passwords introduced matches the one from DB.
    user is an instance of the `User` class.
    """
    form = LoginForm(request.form)

    if request.method == 'POST':
        users = mongo.db.users
        user_login = users.find_one({'email': request.form['email']})

        if user_login and User.validate_login(user_login['password'], request.form["password"]):
            user_obj = User(email=user_login['email'])
            login_user(user_obj)
            next = request.args.get('next')
            flash('You logged in successfully!','success')
            return redirect(next or url_for('dashboard'))
        
        flash('Email or password is wrong. Try again!', 'danger')
        return redirect(url_for('login'))
            
    return render_template('login.html', form=form)

#User logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get('PORT')),
            debug=False)
