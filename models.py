from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    first_name = db.Column(db.String(50),
    nullable =False
    )

    last_name = db.Column(db.String(50),
    nullable =False
    )

    profile_url = db.Column(db.String(300),
    default = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
    
    )
class Post(db.Model):

    __tablename__ = "posts"
    creator = db.relationship('User',backref='created_by')
    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    title = db.Column(db.String(50),
    nullable = False, unique = True)

    content = db.Column(db.String(1000))

    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tags = db.relationship('Tag', secondary="posttags",backref="posts")

    # test
    # tags = db.relationship('Tag')

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    name = db.Column(db.String(50),
    nullable = False)

class PostTag(db.Model):

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)
