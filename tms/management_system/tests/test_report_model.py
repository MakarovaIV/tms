import datetime

from django.test import TestCase

from ..models import CustomUser, TP, Report


class TestReport(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.plan = TP.objects.create(name='Test plan',
                                      desc='How to test plan',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      status="IN PROGRESS",
                                      modification_date=datetime.datetime.now())
        self.report = Report.objects.create(name='Test report',
                                            plan=self.plan,
                                            user=self.customuser)

    def tearDown(self) -> None:
        self.report.delete()
        self.plan.delete()
        self.customuser.delete()

    def test_report_model(self):
        self.assertTrue(isinstance(self.report.name, str))
        self.assertEqual(self.report.name, 'Test report')
        self.assertEqual(self.report.plan.name, 'Test plan')
        self.assertEqual(self.report.user.username, 'TestUser')
