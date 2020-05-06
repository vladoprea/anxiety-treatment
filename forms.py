import os
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.validators import DataRequired, EqualTo


#Register Form Class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', validators=[DataRequired('Choose a Password')])
    confirm = PasswordField('Confirm Password', validators=[
                            DataRequired('Please re-type your Password'), EqualTo('password')])

#Login Form Class
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])

#Journal Entry Class
class JournalForm(Form):
    title = StringField('Title', [validators.Length(min=3, max=100)])
    body = TextAreaField('Description')

#TFB Cycle Entry Class
class ToughtsForm(Form):
    situation = StringField('Situation', [validators.Length(min=3)])
    feeling = StringField('Feeling')
    rate_feeling = SelectField(u'Rate Feeling', choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    physical = StringField('Physical Reaction')
    behaviour = StringField('Behaviours')
    hot_tought = StringField('Hot Tought')
    evidence = TextAreaField('Evidence that support the hot tought')
    counter_evidence = TextAreaField('Counter Evidence for the hot tought')
    alternative = TextAreaField('Alternative/Balanced toughts')