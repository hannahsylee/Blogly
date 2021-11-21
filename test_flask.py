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

class BloglyViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="Hannah", last_name="Lee")

        Post.query.delete()

        post = Post(title="Corgi", content="Corgi Cute", user_id=1)

        db.session.add(user)
        db.session.add(post)

        db.session.commit()

        self.user_id = user.id

        # self.user_id = 1

        # post = Post(title="Corgi", content="Corgi Cute", user_id=1)

        # db.session.add(post)
        # # db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hannah Lee', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Hannah Lee</h1>', html)

    # def test_add_user(self):
    #     with app.test_client() as client:
    #         d = {"first_name": "Samantha", "last_name": "Williams"}
    #         resp = client.post("/users", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<li>Samantha Williams</li>", html)

    # Part Two
    # def test_list_posts(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/users/{self.user_id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('Corgi', html)

    # def test_show_post(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/posts/{self.post_id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h1>Corgi</h1>', html)

    # def test_add_user(self):
    #     with app.test_client() as client:
    #         d = {"first_name": "Samantha", "last_name": "Williams"}
    #         resp = client.post("/users", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<li>Samantha Williams</li>", html)
