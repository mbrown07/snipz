from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager, utils

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    def get_id(self):
        return self.username

class CodeSnippet(db.Document):
    author = db.ReferenceField('User', required=True)
    title = db.StringField(min_length=1, max_length=100)
    code = db.StringField(required=True)
    language = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=50))
    difficulty = db.StringField(choices=['Easy', 'Medium', 'Hard'])
    created_at = db.DateTimeField(default=utils.current_time())
    likes = db.ListField(db.StringField(), default=list)
    dislikes = db.ListField(db.StringField(), default=list)

class Review(db.Document):
    commenter = db.ReferenceField('User', required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True, default=utils.current_time())
    snippet_id = db.StringField(required=True)
    snippet_title = db.StringField(required=True, min_length=1, max_length=100)
    image = db.StringField()

class Snippet(db.Document):
    user = db.ReferenceField('User', required=True)
    snippet = db.ReferenceField('CodeSnippet', required=True)