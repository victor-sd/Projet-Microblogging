from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, validators,BooleanField,SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length,Email

class UserForm(FlaskForm):
    username = StringField('Username', validators=[
                       DataRequired(), Length(min=3, max=20)])
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=20)])
    firstname = StringField('Firstname', validators=[
                       DataRequired(), Length(min=3, max=20)])
    mail = StringField('Email Address', validators=[
                       DataRequired(), Email(message='invalid email'), Length(min=3, max=30)])
    mdp = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')