from django.test import TestCase , Client
from django.urls import reverse
from accounts.models import User 
from finance.models import Category


class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='teste@email.com',
            password='123456'
        )
        session = self.client.session
        session['user_id'] = self.user.id_user
        session.save()
        self.create_url = reverse('create_category')
    

    ## 1º test case : register successfully
    def test_register_successfully(self):
        
        response = self.client.post(self.create_url,{
            'name':'Test Category',
            'user':self.user.id_user
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_categories'))

    ## 2º test case : register with existing category name
    def test_register_with_existing_category_name(self):
        Category.objects.create(name='Test Category', user=self.user)

        response = self.client.post(self.create_url,{
            'name':'Test Category',
            'user':self.user.id_user
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this category already exists")

        count = Category.objects.filter(name='Test Category').count()
        self.assertEqual(count, 1)

    ## Test na list of categories
    def test_list_categories(self):
        Category.objects.create(name='Category 1', user=self.user)
        Category.objects.create(name='Category 2', user=self.user)

        list_url = reverse('list_categories')
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category 1')
        self.assertContains(response, 'Category 2')