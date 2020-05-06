import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.validators import DataRequired, EqualTo, Length


#Register Form Class
class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [Length(min=4, max=25)])
    email = StringField('Email', validators = [Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

#Login Form Class
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [Length(min=6, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])

#Journal Entry Class
class JournalForm(FlaskForm):
    title = StringField('Title', validators = [Length(min=4)])
    body = TextAreaField('Description')

#TFB Cycle Entry Class
class ToughtsForm(FlaskForm):
    situation = StringField('Situation', validators = [Length(min=4)])
    feeling = StringField('Feeling')
    rate_feeling = SelectField(u'Rate Feeling', choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    physical = StringField('Physical Reaction')
    behaviour = StringField('Behaviours')
    hot_tought = StringField('Hot Tought')
    evidence = TextAreaField('Evidence that support the hot tought')
    counter_evidence = TextAreaField('Counter Evidence for the hot tought')
    alternative = TextAreaField('Alternative/Balanced toughts')