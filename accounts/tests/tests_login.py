from django.test import TestCase , Client
from django.urls import reverse
from accounts.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    ## 1º test case : login successfully with email
    def test_login_with_email_successfully(self):
        User.objects.create(
            username='testuser',
            email='teste@email.com',
            password='123456')
        
        response = self.client.post(self.login_url, {
            'login': 'teste@email.com',
            'password': '123456'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
    
    ## 2º test case : login successfully with username
    def test_login_with_username_successfully(self):
        User.objects.create(
            username='testuser',
            email='teste@email.com',
            password='123456')
        
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': '123456'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
    
    ## 3º test case : login with wrong password
    def test_login_with_wrong_password(self):
        User.objects.create(
            username='testuser',
            email='teste@email.com',
            password='123456')
        
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email ou password errados")
    
    ## 4º test case : login with non-existing user
    def test_login_with_non_existing_user(self):
        response = self.client.post(self.login_url, {
            'login': 'nonexistinguser',
            'password': '123456'
        })

        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "Email ou password errados")  



   

