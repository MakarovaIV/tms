from django.test import TestCase

from ..models import CustomUser, Project, Suit


class TestSuit(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.project = Project.objects.create(name='Test project',
                                              desc='How to test project',
                                              user=self.customuser)
        self.suit = Suit.objects.create(name='Test suit',
                                        desc='How to test suit',
                                        user=self.customuser,
                                        proj=self.project,
                                        modified_by=self.customuser.id)

    def tearDown(self) -> None:
        self.suit.delete()
        self.project.delete()
        self.customuser.delete()

    def test_suit_model(self):
        self.assertTrue(isinstance(self.suit.name, str))
        self.assertEqual(self.suit.name, 'Test suit')
        self.assertTrue(isinstance(self.suit.desc, str))
        self.assertEqual(self.suit.desc, 'How to test suit')
        self.assertEqual(self.suit.proj.name, 'Test project')
        self.assertEqual(self.suit.user.username, 'TestUser')
        self.assertEqual(self.suit.modified_by, self.customuser.id)
