from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test import Client

from ..models import CustomUser, Project, Suit


class TestSuitCreateView(TestCase):
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

    def test_suit_create(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='testuser', password='q1w2e3r4t5y61')
        response = c.post('/projects/' + str(self.project.id) + '/suit/create/',
                          {'name': 'Suit 1',
                           'desc': 'Description for project 1'},
                          follow=True)
        self.assertEqual(response.status_code, 200)
        project_name = get_object_or_404(Project, name='Project 1').name
        self.assertEqual(project_name, 'Project 1')


class TestSuitListView(TestCase):
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

    def test_suit_list(self):
        response = self.client.get('/projects/' + str(self.project.id) + '/suits/')
        self.assertTemplateUsed(response, template_name='management_system/suits/suit_list.html')


class TestSuitUpdateView(TestCase):
        def setUp(self) -> None:
            self.customuser = CustomUser.objects.create(username='testuser',
                                                        email='testuser@mail.ru',
                                                        type='Tester')
            self.customuser.set_password('q1w2e3r4t5y61')
            self.customuser.save()
            self.project = Project.objects.create(name='Project 1',
                                                  desc='How to test project',
                                                  user=self.customuser)
            self.suit = Suit.objects.create(name='Suit 1',
                                            desc='How to test suit',
                                            user=self.customuser,
                                            proj=self.project,
                                            modified_by=self.customuser.id)

        def tearDown(self) -> None:
            self.suit.delete()
            self.project.delete()
            self.customuser.delete()

        def test_suit_update(self):
            c = Client()
            Client(enforce_csrf_checks=True)
            c.login(username='testuser', password='q1w2e3r4t5y61')
            response = c.post('/projects/' + str(self.project.id)
                              + '/suit/update/' + str(self.suit.id)
                              + '/',
                              {'name': 'Suit 1 rename',
                               'desc': 'How to test suit'},
                              follow=False)
            suit_renamed = get_object_or_404(Suit, id=self.suit.id)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(suit_renamed.name, 'Suit 1 rename')
