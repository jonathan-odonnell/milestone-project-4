from django.http import response
from django.test import TestCase
from .models import NewsletterSignUp

class TestHomeViews(TestCase):
    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_can_add_newsletter_signup(self):
        response = self.client.post('/', {
           ' newsletter': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)

class TestHomeModels(TestCase):
    def test_newsletter_signup_string_method(self):
        email = NewsletterSignUp(email='test@example.com')
        self.assertEqual(str(email), 'test@example.com')
