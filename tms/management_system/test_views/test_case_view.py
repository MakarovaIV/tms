from django.test import TestCase
from django.test import Client

from ..models import CustomUser, Project, Suit, TC

STEPS = [{"index": "0", "step_name": "Step name", "step_value": "Expected result"}, {"index": "1", "step_name": "sdvg", "step_value": "xcncvn "}]


class TestCaseCreateView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()
        self.project = Project.objects.create(name='Project 1',
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

    def test_case_create(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='testuser', password='q1w2e3r4t5y61')
        response = c.post('/projects/' + str(self.project.id) + '/suit/' + str(self.suit.id) + '/tc/',
                          {'name': 'Test case 1',
                           'desc': 'How to test case',
                           'status': 'ACTIVE',
                           'steps': STEPS},
                          follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='management_system/test_cases/test_cases_form.html')


class TestCaseListView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()
        self.project = Project.objects.create(name='Project 1',
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

    def test_case_list(self):
        response = self.client.get('/projects/' + str(self.project.id)
                                   + '/suit/' + str(self.suit.id)
                                   + '/',)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='management_system/test_cases/test_cases_list.html')


class TestCaseUpdateView(TestCase):
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
        self.suit = Suit.objects.create(name='Test suit',
                                        desc='How to test suit',
                                        user=self.customuser,
                                        proj=self.project,
                                        modified_by=self.customuser.id)
        self.case = TC.objects.create(name='Test case',
                                      desc='How to test case',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      proj=self.project,
                                      suit=self.suit,
                                      status="ACTIVE",
                                      steps=STEPS)

    def tearDown(self) -> None:
        self.case.delete()
        self.suit.delete()
        self.project.delete()
        self.customuser.delete()

    def test_case_update(self):
            c = Client()
            Client(enforce_csrf_checks=True)
            c.login(username='testuser', password='q1w2e3r4t5y61')
            response = c.post('/projects/' + str(self.project.id)
                              + '/suit/' + str(self.suit.id)
                              + '/tc/' + str(self.case.id)
                              + '/',
                              {'name': 'Test case 1 rename'},
                              follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name='management_system/test_cases/test_cases_form.html')


class TestCaseDetailView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()
        self.project = Project.objects.create(name='Project 1',
                                              desc='How to test project',
                                              user=self.customuser)
        self.suit = Suit.objects.create(name='Test suit',
                                        desc='How to test suit',
                                        user=self.customuser,
                                        proj=self.project,
                                        modified_by=self.customuser.id)
        self.case = TC.objects.create(name='Test case',
                                      desc='How to test case',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      proj=self.project,
                                      suit=self.suit,
                                      status="ACTIVE",
                                      steps=STEPS)

    def tearDown(self) -> None:
        self.case.delete()
        self.suit.delete()
        self.project.delete()
        self.customuser.delete()

    def test_case_detail(self):
        response = self.client.get('/projects/' + str(self.project.id)
                                   + '/suit/' + str(self.suit.id)
                                   + '/tc/' + str(self.case.id)
                                   + '/detail/')
        self.assertTemplateUsed(response, template_name='management_system/test_cases/test_cases_detail.html')
