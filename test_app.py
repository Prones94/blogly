import unittest
from app import app
from models import db, User

# Uses an in-memory SQLite database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLAlCHEMY_ECHO'] = False
app.config['TESTING'] = True

class UserTestCase(unittest.TestCase):
  def setUp(self):
    """Set up test database and create tables"""
    self.clients = app.test_client()
    db.create_all()

    # Add sample data
    user1 = User(first_name="Test", last_name="User1", image_url=None)
    user2 = User(first_name="Test", last_name="User2", image_url=None)
    db.session.add_all([user1, user2])
    db.session.commit()

  def tearDown(self):
    """Clean up the database after each test"""
    db.session.remove()
    db.drop_all()

  def test_list_users(self):
    """Test that the /users route shows the user list"""
    res = self.client.get('/users')
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'Test User1', res.data)
    self.assertIn(b'Test User2', res.data)

  def test_show_user(self):
    """Test that the user detail page displays correct information"""
    user = User.query.first()
    res = self.client.get(f'/users/{user.id}')
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'Test User1', res.data)

  def test_add_user(self):
    """Test that a new user can be added successfully"""
    res = self.client('/users/new', data={
      'first_name': 'Updated',
      'last_name': 'User',
      'image_url': ''
    }, follow_redirects=True)
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'Updated User', res.data)

  def test_delete_user(self):
    """Test that a user can be deleted successfully"""
    user = User.query.first()
    res = self.client.post(f'/users/{user.id}/delete', follow_redirects=True)
    self.assertEqual(res.status_code, 200)
    self.assertNotIn(b'Test User1', res.data)
