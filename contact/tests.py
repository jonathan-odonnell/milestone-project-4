from django.test import TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import CustomerContact
from .forms import ContactForm


class TestContactViews(TestCase):
    def setUp(self):
        """
        Sets up the user and email address. Code for creating the users is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/,
        code for creating the email address is from
        https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py
        """
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
        """
        Verifies that a status of 200 is returned and the contact template was
        used when an anonymous user tries and access the contact page
        """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_get_logged_in_user_contact_page(self):
        """
        Logs in the user and verifies that a status of 200 is returned and
        the contact template was used when an anonymous user tries and access
        the contact page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_can_submit_contact_form(self):
        """
        Verifies that a status of 200 is returned and a new customer contact is
        created in the database when a post request with valid customer contact
        details is submitted to the contact page.
        """
        response = self.client.post('/contact/', {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Offers',
            'message': 'This is a test message',
        })
        self.assertEqual(response.status_code, 200)
        customer_contact = CustomerContact.objects.filter(
            email='test@example.com')
        self.assertEqual(len(customer_contact), 1)


class TestContactForm(TestCase):
    def test_all_form_fields_required(self):
        """Tests the required fields in the contact form"""
        form = ContactForm({
            'full_name': '',
            'email': '',
            'subject': '',
            'message': '',
        })
        self.assertEqual(form.errors['full_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'This field is required.')
        self.assertEqual(form.errors['subject'][0], 'This field is required.')
        self.assertEqual(form.errors['message'][0], 'This field is required.')

    def test_form_invalid_email_input(self):
        """Tests invalid email address input in the contact form"""
        form = ContactForm({
            'full_name': 'Test User',
            'email': 'This is not an email address',
            'subject': 'Offers',
            'message': 'This is a test message',
        })
        self.assertEqual(form.errors['email'][0],
                         'Enter a valid email address.')

    def test_excluded_in_form_metaclass(self):
        """Tests the excluded attribute of the contact form meta class"""
        form = ContactForm()
        self.assertEqual(form.Meta.exclude, ('date',))


class TestContactModels(TestCase):
    def test_customer_contact_string_method(self):
        """
        Creates a customer contact and verifies that the string
        method is correct
        """
        customer_contact = CustomerContact.objects.create(
            full_name='Test User',
            email='test@example.com',
            subject='Offers',
            message='This is a test message',
        )
        self.assertEqual(str(customer_contact), 'Test User - Offers')
