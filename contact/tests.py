from django.test import TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import CustomerContact
from .forms import ContactForm

class TestContactViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

    def test_get_anonymous_user_contact_page(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_get_logged_in_user_contact_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_can_submit_contact_form(self):
        response = self.client.post('/contact/', {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Offers',
            'message': 'This is a test message',
        })
        self.assertEqual(response.status_code, 200)
        customer_contact = CustomerContact.objects.get(email='test@example.com')
        self.assertEqual(customer_contact.full_name, 'Test User')
        self.assertEqual(customer_contact.subject, 'Offers')
        self.assertEqual(customer_contact.message, 'This is a test message')
        self.assertEqual(str(customer_contact), 'Test User - Offers')  


class TestContactForm(TestCase):
    def test_all_form_fields_required(self):
        form = ContactForm({
            'full_name': '',
            'email': '',
            'subject': '',
            'message': '',
        })
        self.assertEqual(form.errors['full_name'][0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'This field is required.')
        self.assertEqual(form.errors['subject'][0], 'This field is required.')
        self.assertEqual(form.errors['message'][0], 'This field is required.')

    def test_form_invalid_email_input(self):
        form = ContactForm({
            'full_name': 'Test User',
            'email': 'This is not an email address',
            'subject': 'Offers',
            'message': 'This is a test message',
        })
        self.assertEqual(form.errors['email'][0], 'Enter a valid email address.')


    def test_excluded_in_form_metaclass(self):
        form = ContactForm()
        self.assertEqual(form.Meta.exclude, ('date',))
