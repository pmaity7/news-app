from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User
from app import app, db

class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    email = StringField('Enter Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email already exists')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=140, max=2000)])
    post = SubmitField('Post')

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=140, max=2000)])
    save = SubmitField('Save')