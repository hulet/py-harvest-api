from unittest import TestCase
from harvest.endpoints import *
from harvest.credentials import PersonalAccessAuthConfigCredential


'''
Harvest API does not provide a sandbox so i will need more time to think about
how to test properly other endpoints
'''


class EndpointsTestCase(TestCase):

    def setUp(self):
        self.credential = PersonalAccessAuthConfigCredential()

    def test_users(self):
        resp = UsersEndpoint(self.credential).get()
        self.assertEqual(resp.status_code, 403)

    def test_users_me(self):
        resp = UsersMeEndpoint(self.credential).get()
        self.assertEqual(resp.status_code, 200)

    def test_usersassignments(self):
        resp = UsersMeEndpoint(self.credential).get()
        user_id = resp.json()['id']
        resp = UsersAssignmentsEndpoint(self.credential, user_id=user_id).get()
        self.assertEqual(resp.status_code, 200)

    def test_projects(self):
        resp = ProjectsEndpoint(self.credential).get()
        self.assertEqual(resp.status_code, 200)

    def test_tasks(self):
        resp = TasksEndpoint(self.credential).get()
        self.assertEqual(resp.status_code, 403)
