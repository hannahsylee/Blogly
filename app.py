"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
def homepage():
    """shows the 5 most recent posts."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# @app.route('/')
# def root():
#     """Homepage redirects to list of users."""

#     return redirect("/users")


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

# Part Two: Adding Posts
@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('posts/new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    # filtering all the tags with ids in tag_ids
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    # flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:id>/')
def show_post(id):
    """Show a post."""
    post = Post.query.get_or_404(id)

    return render_template('posts/post_detail.html', post=post)

@app.route('/posts/<int:id>/edit')
def show_edit_post(id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(id)
    # need to get all tags not just the post's tags.
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:id>/edit', methods=['POST'])
def edit_post(id):
    """Process the edit form, returning the user to the /users page"""
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{id}/')

@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    """Delete the user."""
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

# Part Three -----------------------------------------------------------------
@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page"""
    tags = Tag.query.all()
    return render_template('/tags/list.html', tags=tags)

@app.route('/tags/new')
def new_tag():
    """Shows a form to add a new tag."""
    posts = Post.query.all()
    return render_template('/tags/add.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Process add form, adds tag, and redirect to tag list."""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:id>')
def detail_tag(id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(id)
    # posts = tag.posts
    return render_template('/tags/show.html', tag=tag)

@app.route('/tags/<int:id>/edit')
def show_edit(id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(id)
    return render_template('/tags/edit.html', tag=tag)

@app.route('/tags/<int:id>/edit', methods=['POST'])
def edit_tag(id):
    """Process the edit form, returning the user to the /users page"""
    tag = Tag.query.get_or_404(id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    """Delete a tag."""
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')















