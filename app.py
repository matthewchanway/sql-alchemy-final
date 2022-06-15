"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()

@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("users-list.html",users=users)

@app.route("/users/new")
def show_add_user_form():
    return render_template("add-user-form.html")

@app.route("/users/new", methods = ["POST"])
def add_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    new_user = User(first_name = first_name, last_name = last_name, profile_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<userid>", methods = ["GET","POST"])
def show_user_info(userid):
    user = User.query.get(userid)
    return render_template("user-detail.html",user=user)

@app.route("/users/<userid>/edit")
def show_edit_form(userid):
    user = User.query.get(userid)
    return render_template("edit-user-info.html",user=user)

@app.route("/users/<userid>/edit", methods = ["POST"])
def handle_edit_form(userid):
    user = User.query.get(userid)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user.first_name = first_name
    user.last_name = last_name
    user.profile_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<userid>/delete", methods = ["GET","POST"])
def delete_user(userid):
    
    User.query.filter(User.id == userid).delete()
    db.session.commit()
    return redirect("/users")

# Part Two Routes

@app.route("/users/<int:userid>/posts/new")
def show_new_post_form(userid):
    user = User.query.get(userid)
    tags = Tag.query.all()
    return render_template("add-post-form.html",user=user, tags=tags)

@app.route("/users/<int:userid>/posts/new", methods = ["POST"])
def add_new_post(userid):
    now = datetime.now()
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist('check')
    new_post = Post(title = title, content=content, created_at=now, user_id = userid )
    db.session.add(new_post)
    db.session.commit()
    for tag in tags:
        new_posttag = PostTag(post_id = new_post.id, tag_id = tag)
        db.session.add(new_posttag)
        db.session.commit()

    return redirect(url_for('show_user_info',userid=userid))

@app.route("/posts/<int:postid>")
def view_post(postid):
    post = Post.query.get(postid)
    
    return render_template("view-post.html",post=post)

@app.route("/posts/<int:postid>/edit")
def show_edit_post_form(postid):
    post = Post.query.get(postid)
    tags = Tag.query.all()
    return render_template("edit-post.html",post=post, tags=tags)

@app.route("/posts/<int:postid>/edit", methods = ["POST"])
def handle_edit_post_from(postid):
    PostTag.query.filter_by(post_id=postid).delete()
    post = Post.query.get(postid)
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist('check')
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    for tag in tags:
        new_posttag = PostTag(post_id = postid, tag_id = tag)
        db.session.add(new_posttag)
        db.session.commit()
    return redirect(url_for('view_post',postid=postid))

@app.route("/posts/<int:postid>/delete", methods = ["POST","GET"])
def handle_delete(postid):
    post = Post.query.get(postid)
    userid = post.user_id
    PostTag.query.filter_by(post_id=postid).delete()
    Post.query.filter_by(id=postid).delete()
    db.session.commit()

    return redirect(url_for('show_user_info',userid=userid))

# Part 3 routes

@app.route("/tags")
def show_tags():
    tags = Tag.query.all()
    return render_template("tags-list.html",tags=tags)

@app.route("/tags/<int:tagid>", methods = ["GET","POST"])
def show_tag_info(tagid):
    tag = Tag.query.get(tagid)
    return render_template("tag-detail.html",tag=tag)

@app.route("/tags/new")
def show_new_tag_form():
    return render_template("add-tag-form.html")

@app.route("/tags/new", methods = ["POST"])
def add_new_tag():
    name = request.form["name"]
    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tagid>/edit")
def show_edit_tag_form(tagid):
    tag = Tag.query.get(tagid)
    return render_template("edit-tag.html", tag=tag)

@app.route("/tags/<int:tagid>/edit", methods = ["POST"])
def handle_edit_tag_form(tagid):
    tag = Tag.query.get(tagid)
    name = request.form["name"]
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tagid>/delete", methods = ["POST","GET"])
def handle_tag_delete(tagid):
    PostTag.query.filter_by(tag_id=tagid).delete()
    tag = Tag.query.get(tagid)
    tagid = tag.id
    Tag.query.filter_by(id=tagid).delete()
    db.session.commit()

    return redirect(url_for('show_tags'))





    
