from django.test import TestCase
from .models import NewsletterSignUp


class TestHomeViews(TestCase):
    def test_get_home_page(self):
        """
        Verifies that a status of 200 is returned and the index template was
        used when the user tries and access the home page
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_can_add_newsletter_signup(self):
        """
        Verifies that a status of 200 is returned and a new newsletter
        sign up is created in the database when a post request with
        valid newsletter sign up details is submitted to the home page.
        """
        response = self.client.post('/newsletter/', {
            ' newsletter': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        newsletter_sign_up = NewsletterSignUp.objects.filter(
            email='test@example.com')
        self.assertEqual(len(newsletter_sign_up), 1)


class TestHomeModels(TestCase):
    def test_newsletter_signup_string_method(self):
        """
        Creates a newsletter sign up and verifies that the string
        method is correct
        """
        newsletter_sign_up = NewsletterSignUp(email='test@example.com')
        self.assertEqual(str(newsletter_sign_up), 'test@example.com')
