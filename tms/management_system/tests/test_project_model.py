from django.test import TestCase

from ..models import CustomUser, Project


class TestProject(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.project = Project.objects.create(name='Test project',
                                              desc='How to test project',
                                              user=self.customuser)

    def tearDown(self) -> None:
        self.project.delete()
        self.customuser.delete()

    def test_project_model(self):
        self.assertTrue(isinstance(self.project.name, str))
        self.assertEqual(self.project.name, 'Test project')
        self.assertTrue(isinstance(self.project.desc, str))
        self.assertEqual(self.project.desc, 'How to test project')
        self.assertEqual(self.project.user.username, 'TestUser')
