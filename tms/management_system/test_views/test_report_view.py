from django.test import TestCase
from django.test import Client

from ..models import CustomUser, Report, TP


class TestReportCreateView(TestCase):
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

    def test_report_create(self):
        c = Client()
        Client(enforce_csrf_checks=True)
        c.login(username='testuser', password='q1w2e3r4t5y61')
        response = c.post('/report/create/',
                          {'name': 'Plan 1',
                           'plan_id': self.plan.id},
                          follow=True)
        self.assertEqual(response.status_code, 200)


class TestReportListView(TestCase):
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
        self.report = Report.objects.create(name='Test report',
                                            plan=self.plan,
                                            user=self.customuser)

    def tearDown(self) -> None:
        self.report.delete()
        self.plan.delete()
        self.customuser.delete()

    def test_report_list(self):
        response = self.client.get('/reports/')
        self.assertTemplateUsed(response, template_name='management_system/reports/report_list.html')


class TestPReportDeleteView(TestCase):
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
        self.report = Report.objects.create(name='Test report',
                                            plan=self.plan,
                                            user=self.customuser)

    def tearDown(self) -> None:
        self.report.delete()
        self.plan.delete()
        self.customuser.delete()

    def test_plan_delete(self):
        response = self.client.get('/report/delete/' + str(self.report.id))
        self.assertEqual(response.status_code, 301)
