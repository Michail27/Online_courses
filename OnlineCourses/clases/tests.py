from django.test import TransactionTestCase
from django.urls import reverse
from clases.models import ProfileUser, Course


class TestMyAppPlease(TransactionTestCase):
    def setUp(self):
        url = reverse('register')
        data = {'username': 'student', 'password': 'useruser', 'email': 'asd@sdv.ru', 'role': 'student'}
        self.user = self.client.post(url, data)
        data1 = {'username': 'student1', 'password': 'useruser', 'email': 'asd@sdv.ru', 'role': 'student'}
        self.user1 = self.client.post(url, data1)
        data3 = {'username': 'teacher', 'password': 'useruser', 'email': 'asd@sdv.ru', 'role': 'teacher'}
        self.user2 = self.client.post(url, data3)

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
            'username': 'user2',
            'password': 'useruser'}

        response = self.client.get(url)
        self.assertEqual(response.status_code, 405, msg='method is not allowed')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200, msg='is not redirect')

        url = reverse('logout')
        self.client.post(url)
        self.assertEqual(response.status_code, 200, msg='logout')

    def test_courses(self):
        url = reverse('login')
        data = {'username': 'student', 'password': 'useruser'}
        self.client.post(url, data)
        url = reverse('courses_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, msg='is not list courses')
        url = reverse('login')
        data = {'username': 'teacher', 'password': 'useruser'}
        self.client.post(url, data)
        data = {'name': 'course', 'teacher_owner': 'teacher', 'teachers': 'teacher', 'students': 'student'}
        url = reverse('courses_list')
        self.client.post(url, data)
        # self.assertTrue(Course.objects.exists(), msg='course is not created')
        course = Course.objects.first()
        self.assertEqual(course.username, data['name'], msg='not equal')
        self.assertEqual(response.status_code, 201, msg='is not created')


