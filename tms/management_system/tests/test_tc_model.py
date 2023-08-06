from django.test import TestCase

from ..models import CustomUser, Project, Suit, TC


STEPS = [{"index": "0", "step_name": "Step name", "step_value": "Expected result"}, {"index": "1", "step_name": "sdvg", "step_value": "xcncvn "}]


class TestCase(TestCase):
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

    def tearDown(self) -> None:
        self.case.delete()
        self.suit.delete()
        self.project.delete()
        self.customuser.delete()

    def test_case_model(self):
        self.assertTrue(isinstance(self.case.name, str))
        self.assertEqual(self.case.name, 'Test case')
        self.assertTrue(isinstance(self.case.desc, str))
        self.assertEqual(self.case.desc, 'How to test case')
        self.assertEqual(self.case.proj.name, 'Test project')
        self.assertEqual(self.case.suit.name, 'Test suit')
        self.assertEqual(self.case.user.username, 'TestUser')
        self.assertTrue(isinstance(self.case.status, str))
        self.assertEqual(self.case.status, 'ACTIVE')
        self.assertEqual(self.case.steps, STEPS)
        self.assertEqual(self.case.modified_by, self.customuser.id)
