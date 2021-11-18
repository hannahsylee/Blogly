"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'blogly'

# db = SQLAlchemy()
# db.app = app
# db.init_app(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")


##############################################################################
# User route

@app.route('/users')
def users_index():
    """Show a page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/listing.html', users=users)

@app.route('/users/new')
def users_new():
    """Show an add form for users"""
    return render_template('users/new_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form['fname']
    last_name = request.form['lname']
    image_url = request.form['imageURL'] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>')
def show_user(id):
    """Show information about the given user."""
    user = User.query.get_or_404(id)
    return render_template("users/user_detail.html", user=user)

@app.route('/users/<int:id>/edit')
def show_edit_form(id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(id)
    return render_template("users/edit.html", user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def edit_user(id):
    """Process the edit form, returning the user to the /users page"""
    user = User.query.get_or_404(id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['imageURL'] 

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """Delete the user."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')









