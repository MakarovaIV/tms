import datetime

from django.test import TestCase

from ..models import CustomUser, TP


class TestPlan(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.plan = TP.objects.create(name='Test plan',
                                      desc='How to test plan',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      status="IN PROGRESS")

    def tearDown(self) -> None:
        self.plan.delete()
        self.customuser.delete()

    def test_plan_model(self):
        self.assertTrue(isinstance(self.plan.name, str))
        self.assertEqual(self.plan.name, 'Test plan')
        self.assertTrue(isinstance(self.plan.desc, str))
        self.assertEqual(self.plan.desc, 'How to test plan')
        self.assertEqual(self.plan.status, 'IN PROGRESS')
        self.assertEqual(self.plan.user.username, 'TestUser')
