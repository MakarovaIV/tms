from django.test import TestCase

from ..models import CustomUser


class TestRegister(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'q1w2e3r4t5y61',
        self.type = 'Tester'

    def test_registry_status_code(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        self.client.post('/signup/', {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            'type': self.type
        })
        users = CustomUser.objects.all()
        self.assertEqual(users.count(), 1)

    def test_signup_page_view_name(self):
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response, template_name='management_system/signup_form.html')


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru')
        self.customuser.set_password('test_pass')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_login_status_code(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        response = self.client.post('/login/', {
            'username': self.customuser.username,
            'password': self.customuser.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_login_page_view_name(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, template_name='management_system/login.html')


class TestLogout(TestCase):
    def test_logout_status_code(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 200)

    def test_logout_page_view_name(self):
        response = self.client.get('/logout/')
        self.assertTemplateUsed(response, template_name='management_system/logout.html')


class TestGetUserImage(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru')
        self.customuser.set_password('test_pass')
        self.customuser.save()

    def test_response_status_code(self):
        response = self.client.get(f'/get_user_image/{self.customuser.pk}/',)
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        self.customuser.delete()
