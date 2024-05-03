from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

class SearchForm(FlaskForm):
    title = StringField("Title", validators=[Length(min=0, max=100)])
    tag = StringField("Tag", validators=[Length(max=100)])
    language = SelectField("Language", choices=[]) 
    difficulty = SelectField("Difficulty", choices=[('None', 'None'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    submit = SubmitField("Search")

class SnippetReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )

    submit = SubmitField("Enter Comment")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(min=1, max=40)])
    submit_username = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Select a different one.')
        pass

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    submit_picture = SubmitField('Update')

class SnippetUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    code = TextAreaField('Code', validators=[DataRequired()])
    language = SelectField('Language', choices=[('Python', 'Python'), ('Java', 'Java'), ('C++', 'C++')])
    tags = StringField('Tags', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    submit = SubmitField('Upload Snippet')

class ShareSnippetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Share')
