from app.models import Pitch,User
from app import db
import unittest


class TestReview(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(title='Pitch for movies',category="movies",post="hooohohhhoooo")

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)


