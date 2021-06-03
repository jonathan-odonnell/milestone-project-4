from django.http import response
from django.test import TestCase
from .models import NewsletterSignUp

class TestHomeForm(TestCase):
    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_item_string_method_returns_email(self):
        email = NewsletterSignUp(email='test@example.com')
        self.assertEqual(str(email), 'test@example.com')
