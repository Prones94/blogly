from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


"""Models for Blogly."""
class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(20), nullable=False)
  image = db.Column(db.String, nullable=False, default='https://via/placeholder.com/150')

  def __repr__(self):
    return f'<User {self.first_name} {self.last_name}>'

  def get_full_name(self):
    """Returns the user's full name."""
    return f'{self.first_name} {self.last_name}'

