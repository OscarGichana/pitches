import unittest
from app.models import User,Comment,Pitch

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.new_comment = Comment(comment = 'rotich',pitch_id=1,user_id=2)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)
