from django.core.files import File
from unittest import mock

from django.test import TestCase

from ..models import CustomUser


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_user_model(self):
        self.assertTrue(isinstance(self.customuser.username, str))
        self.assertEqual(self.customuser.username, 'TestUser')
        self.assertTrue(isinstance(self.customuser.email, str))
        self.assertEqual(self.customuser.email, 'testuser@mail.ru')
        self.assertTrue(isinstance(self.customuser.password, str))
        self.assertEqual(self.customuser.password, 'test_pass')

    def test_file_field(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        file_model = CustomUser(picture=file_mock)
        self.assertEqual(file_model.picture.name, file_mock.name)