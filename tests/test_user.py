import unittest
from app.models import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(username = 'rotich',email = 'jjd@gmail.com',secure_password = 'banana', bio='you got this,he got this',profile_pic_path='/static/demo.png')

    def test_password_setter(self):
        self.assertTrue(self.new_user.secure_password is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.secure_password)



