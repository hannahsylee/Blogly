"""Seed file to make sample data for db."""

from models import db, connect_db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

PostTag.query.delete()
User.query.delete()
Post.query.delete()
Tag.query.delete()

# Add sample users and posts
Hannah = User(first_name='Hannah', last_name='Lee')
Sarah = User(first_name='Sarah', last_name='Park')
John = User(first_name='John', last_name='Doe')

# Post
corgi = Post(title='Corgi', content='Corgis are cute', user_id=Hannah.id)
terrier = Post(title='Terrier', content='Looks like grandpa', user_id=Hannah.id)
cat = Post(title='Cat', content="Doggy cat", user_id=Sarah.id)
missing = Post(title='Missing', content='Missing person with no name', user_id=John.id)

db.sesson.add_all([Hannah, Sarah, John, corgi, terrier, cat, missing])
db.session.commit()






