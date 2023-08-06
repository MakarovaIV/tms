from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test import Client

from ..models import CustomUser, Project


class TestProjectCreateView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_project_create(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='testuser', password='q1w2e3r4t5y61')
        response = c.post('/project/create/',
                          {'name': 'Project 1',
                           'desc': 'Description for project 1'},
                          follow=True)
        self.assertEqual(response.status_code, 200)
        project_name = get_object_or_404(Project, name='Project 1').name
        self.assertEqual(project_name, 'Project 1')


class TestProjectListView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_project_list(self):
        response = self.client.get('/projects/')
        self.assertTemplateUsed(response, template_name='management_system/projects/project_list.html')


class TestProjectUpdateView(TestCase):
        def setUp(self) -> None:
            self.customuser = CustomUser.objects.create(username='testuser',
                                                        email='testuser@mail.ru',
                                                        type='Tester')
            self.customuser.set_password('q1w2e3r4t5y61')
            self.customuser.save()
            self.project = Project.objects.create(name='Project 1',
                                                  desc='How to test project',
                                                  user=self.customuser)

        def tearDown(self) -> None:
            self.project.delete()
            self.customuser.delete()

        def test_project_update(self):
            c = Client()
            Client(enforce_csrf_checks=True)
            c.login(username='testuser', password='q1w2e3r4t5y61')
            response = c.post('/project/update/' + str(self.project.id) + '/',
                              {'name': 'Project 1 rename',
                               'desc': self.project.desc},
                              follow=False)
            project_renamed = get_object_or_404(Project, id=self.project.id)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(project_renamed.name, 'Project 1 rename')

