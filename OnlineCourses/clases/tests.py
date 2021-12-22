from django.test import TestCase, TransactionTestCase
from rest_framework.reverse import reverse

from clases.models import ProfileUser


class TestMyAppPlease(TransactionTestCase):
    def setUp(self):
        data = {'username': 'student1', 'password': 'useruser', 'email': 'asd@sdv.ru', 'role': 'student'}
        self.user = ProfileUser.objects.create_user(data)
        data1 = {'username': 'user', 'password': 'useruser', 'email': 'asd@sdv1.ru', 'role': 'teacher'}
        self.user1 = ProfileUser.objects.create_user(data1)
        data2 = {'username': 'student2', 'password': 'useruser', 'email': 'asd@sdv2.ru', 'role': 'student'}
        self.user2 = ProfileUser.objects.create_user(data2)

    def test_register(self):
        url = reverse('register')
        data = {
            'username': 'user1',
            'password': 'useruser',
            'email': 'asd@sdv.ru',
            'role': 'student'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, msg='is not redirect')
        self.assertTrue(ProfileUser.objects.exists(), msg='user is not created')
        data = {
            'username': 'user2',
            'password': 'useruser',
            'email': 'asd@sdv.ru',
            'role': 'teacher'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, msg='is not redirect')
        self.assertTrue(ProfileUser.objects.exists(), msg='user is not created')

    def test_no_register(self):
        url = reverse('register')
        data = {
            'username': 'user3',
            'password': 'useruser',
            'email': 'asd@sdv.ru'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400, msg='is not redirect')


    def test_login_logout(self):
        url = reverse('register')
        data = {
            'username': 'user1',
            'password': 'useruser',
            'email': 'asd@sdv.ru',
            'role': 'student'
        }
        self.client.post(url, data)
        data = {
            'username': 'user2',
            'password': 'useruser',
            'email': 'asd@sdv.ru',
            'role': 'teacher'
        }
        self.client.post(url, data)
        self.assertEqual(ProfileUser.objects.count(), 5, msg='created 2 user')

        url = reverse('login')
        data = {
            'username': 'user',
            'password': 'useruser'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401, msg='is not login')
        data = {
            'username': 'user1',
            'password': 'useruser'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200, msg='is not login')

        url = reverse('logout')
        self.client.post(url)

    def test_courses(self):
        url = reverse('register')
        data = {
            'username': 'user1',
            'password': 'useruser',
            'email': 'asd@sdv.ru',
            'role': 'student'
        }
        self.client.post(url, data)
        data = {
            'username': 'user2',
            'password': 'useruser',
            'email': 'asd@sdv.ru',
            'role': 'teacher'
        }
        self.client.post(url, data)



