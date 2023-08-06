from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test import Client

from ..models import CustomUser, Project, TP


class TestPlanCreateView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_plan_create(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='testuser', password='q1w2e3r4t5y61')
        response = c.post('/plan/create/',
                          {'name': 'Plan 1',
                           'desc': 'Description for plan 1',
                           'status': "IN PROGRESS"},
                          follow=True)
        self.assertEqual(response.status_code, 200)


class TestPlanListView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()

    def tearDown(self) -> None:
        self.customuser.delete()

    def test_plan_list(self):
        response = self.client.get('/plans/')
        self.assertTemplateUsed(response, template_name='management_system/test_plans/plan_list.html')


class TestPlanUpdateView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()
        self.plan = TP.objects.create(name='Test plan',
                                      desc='How to test plan',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      status="IN PROGRESS")

    def tearDown(self) -> None:
        self.plan.delete()
        self.customuser.delete()

    # def test_plan_update(self):
    #     c = Client()
    #     Client(enforce_csrf_checks=True)
    #     c.login(username='testuser', password='q1w2e3r4t5y61')
    #     response = c.post('plan/update/' + str(self.plan.id) + '/',
    #                       {'name': 'Plan 1 rename'},
    #                       follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name='management_system/test_plans/plan_form.html')


class TestPlanDeleteView(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='testuser',
                                                    email='testuser@mail.ru',
                                                    type='Tester')
        self.customuser.set_password('q1w2e3r4t5y61')
        self.customuser.save()
        self.plan = TP.objects.create(name='Test plan',
                                      desc='How to test plan',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      status="IN PROGRESS")

    def tearDown(self) -> None:
        self.plan.delete()
        self.customuser.delete()

    def test_plan_delete(self):
        response = self.client.get('/plan/delete/' + str(self.plan.id))
        self.assertEqual(response.status_code, 301)
