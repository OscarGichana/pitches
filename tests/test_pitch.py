from app.models import Review,User
from app import db
import unittest


class TestReview(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James',secure_password = 'potato', email = 'james@ms.com')
        self.new_pitch = Pitch(title='Pitch for movies',category="movies"post="hooohohhhoooo",user = self.user_James )

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)


