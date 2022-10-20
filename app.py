"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
toolbar = DebugToolbarExtension(app)

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home():
    return redirect("/users")


@app.route("/users")
def list_users():
    """list of users and option to add user"""

    users = User.query.all()
    return render_template("users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_user_form():
    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def add_user():
    """add user and redirect to list"""
    new_user = User(
    first_name = request.form['first_name'],
    last_name = request.form['last_name'],
    image_url = request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user-id>")
def user_info(user_id):
    user = User.query.get(user_id)
    return render_template("users/show.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('users/edit.html', user=user)


@app.route("/users/<int:user-id>/edit")
def update_user(user_id):

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user-id/delete", method=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
