from django.test import TestCase , Client
from django.urls import reverse
from accounts.models import User


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    ## 1º test case : register a new user successfully
    def test_register_user_successfully(self):            
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'teste@email.com',
            'password': '123456'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

        user_exists = User.objects.filter(email='teste@email.com').exists()
        self.assertTrue(user_exists)

    ## 2º teste : register with an already registered email
    def test_register_with_existing_email(self):
        User.objects.create(
            username='testuser',
            email='teste@email.com',
            password='123456')
        
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'teste@email.com',
            'password': '123456'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email is already registered.")

        count = User.objects.filter(email='teste@email.com').count()
        self.assertEqual(count, 1)

