from django.test import TestCase

from ..models import CustomUser, Project, Suit, TC, TCHistory


STEPS = [{"index": "0", "step_name": "Step name", "step_value": "Expected result"}, {"index": "1", "step_name": "sdvg", "step_value": "xcncvn "}]


class TestCaseHistory(TestCase):
    def setUp(self) -> None:
        self.customuser = CustomUser.objects.create(username='TestUser',
                                                    email='testuser@mail.ru',
                                                    password='test_pass')
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
        self.case_history = TCHistory.objects.create(name='Test case_history',
                                                     desc='How to test case_history',
                                                     user=self.customuser,
                                                     modified_by=self.customuser.id,
                                                     proj=self.project,
                                                     suit=self.suit,
                                                     status="OUTDATED",
                                                     steps=STEPS,
                                                     tc=self.case)

    def tearDown(self) -> None:
        self.case_history.delete()
        self.case.delete()
        self.suit.delete()
        self.project.delete()
        self.customuser.delete()

    def test_case_history_model(self):
        self.assertTrue(isinstance(self.case_history.name, str))
        self.assertEqual(self.case_history.name, 'Test case_history')
        self.assertTrue(isinstance(self.case_history.desc, str))
        self.assertEqual(self.case_history.desc, 'How to test case_history')
        self.assertEqual(self.case_history.proj.name, 'Test project')
        self.assertEqual(self.case_history.suit.name, 'Test suit')
        self.assertEqual(self.case_history.tc.name, 'Test case')
        self.assertEqual(self.case_history.user.username, 'TestUser')
        self.assertTrue(isinstance(self.case_history.status, str))
        self.assertEqual(self.case_history.status, 'OUTDATED')
        self.assertEqual(self.case_history.steps, STEPS)
        self.assertEqual(self.case_history.modified_by, self.customuser.id)
