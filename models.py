from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


"""Models for Blogly."""
class User(db.Model):
  """Site user"""
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(20), nullable=False)
  image = db.Column(db.String, nullable=False, default='https://via/placeholder.com/150')

  posts = db.relationship("Post", backref="user", cascade="all,delete-orphan")

  @property
  def __repr__(self):
    return f'<User {self.first_name} {self.last_name}>'

  @property
  def get_full_name(self):
    """Returns the user's full name."""
    return f'{self.first_name} {self.last_name}'

class Post(db.Model):
  """Blog Post"""

  __tablename__= "posts"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  @property
  def friendly_date(self):
    """Returns formatted date"""
    return self.created_at.strfttime("%a %b %-d %Y, %-I:%M %p")

class POStTag(db.Model):
  """Tag on a post"""
  __tablename__ = "posts_tags"

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
  """Tag that can be added to posts."""
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable=False, unique=True)

  posts = db.relationship(
    'Post',
    secondary="posts_tags",
    backref="tags",
    # cascade="all,delete"
  )

def connect_db(app):
  """Connects database to Flask app"""
  db.app = app
  db.init_app(app)