from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests views for Users"""

    def setUp(self):
        """Add sample user"""
        User.query.delete

        user = User(first_name="Test", last_name="User", 
        profile_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Test',html)
            self.assertIn('User',html)
    
    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('Test',html)
            self.assertIn('User',html)

    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('Create a user',html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name":"Test2", "last_name":"User2", "image_url": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}
            resp = client.post("/users/new", data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Test2',html)
            self.assertIn('User2',html)

    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         resp = client.post("/users/2/delete", follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code,200)
    #         self.assertNotIn('ID: 2',html)
           
    def test_create_post(self):
        with app.test_client() as client:
            d = {"title":"Matttest", "content":"well done"}
            resp = client.post("/users/2/posts/new", data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Matttest',html)
            

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title":"editpost", "content":"edited"}
            resp = client.post("/posts/1/edit", data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('editpost',html)
           





    
