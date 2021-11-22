"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime    

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
    posts = db.relationship('Post', backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Posts Table"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
    )
    # relation with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # direct navigation: post -> posttag & back
    # post_posttag = db.relationship('PostTag', backref='posts')
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class PostTag(db.Model):
    """joins together a Post and a Tag"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag Table"""

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    # direct navigation: tag -> post & back
    posts = db.relationship('Post',
                            secondary='post_tag',
                            backref='tags')

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)