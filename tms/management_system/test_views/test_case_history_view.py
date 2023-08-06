from django.test import TestCase
from django.test import Client

from ..models import CustomUser, Project, Suit, TC, TCHistory

STEPS = [{"index": "0", "step_name": "Step name", "step_value": "Expected result"}, {"index": "1", "step_name": "sdvg", "step_value": "xcncvn "}]


class TestCaseHistoryListView(TestCase):
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

    def test_case_history_list(self):
        response = self.client.get('/projects/' + str(self.project.id)
                                   + '/suit/' + str(self.suit.id)
                                   + '/tc_history/' + str(self.case.id)
                                   + '/',)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='management_system/tc_history/tc_history_list.html')

    def test_case_history_detail(self):
        response = self.client.get('/projects/' + str(self.project.id)
                                   + '/suit/' + str(self.suit.id)
                                   + '/tc_history/' + str(self.case.id)
                                   + '/detail/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='management_system/tc_history/tc_history_detail.html')

