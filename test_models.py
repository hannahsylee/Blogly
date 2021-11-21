from unittest import TestCase

from app import app

from models import db, connect_db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_models_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyModelTests(TestCase):

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        user = User(first_name="Hannah", last_name="Lee")
        self.assertEquals(user.full_name, "Hannah Lee")

    # def test_get_by_name(self):
    #     user = User(first_name="Hannah", last_name="Lee")
    #     db.session.add(user)
    #     db.session.commit()

    #     dogs = User.get_by_species('dog')
    #     self.assertEquals(dogs, [pet])



    