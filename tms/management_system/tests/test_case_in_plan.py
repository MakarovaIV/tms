from django.test import TestCase

from ..models import CustomUser, Project, Suit, TC, TP, TCinTP


STEPS = [{"index": "0", "step_name": "Step name", "step_value": "Expected result"}, {"index": "1", "step_name": "sdvg", "step_value": "xcncvn "}]


class TestCaseInPlan(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
        self.plan = TP.objects.create(name='Test plan',
                                      desc='How to test plan',
                                      user=self.customuser,
                                      modified_by=self.customuser.id,
                                      status="IN PROGRESS")
        self.project = Project.objects.create(name='Test project',
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
        self.case_in_plan = TCinTP.objects.create(tc=self.case,
                                                  plan=self.plan,
                                                  assignee=self.customuser,
                                                  tc_status="FAILED")

    def tearDown(self) -> None:
        self.case_in_plan.delete()
        self.case.delete()
        self.suit.delete()
        self.project.delete()
        self.customuser.delete()

    def test_case_in_plan_model(self):
        self.assertEqual(self.case_in_plan.tc.name, 'Test case')
        self.assertEqual(self.case_in_plan.plan.name, 'Test plan')
        self.assertEqual(self.case_in_plan.assignee.username, 'TestUser')
        self.assertTrue(isinstance(self.case_in_plan.tc_status, str))
        self.assertEqual(self.case_in_plan.tc_status, 'FAILED')
