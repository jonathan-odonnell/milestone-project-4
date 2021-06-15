from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import Extra
from .forms import ExtraForm
from decimal import Decimal


class TestExtrasViews(TestCase):
    def setUp(self):
        """
        Sets up the users, email addresses, image and extra. Code for creating
        the users is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/,
        code for creating the email addresses is from
        https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py
        and code for the image is from
        https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
        """
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Password',
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=self.superuser,
            email=self.superuser.email
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

        self.image = SimpleUploadedFile(name='test_image.jpg', content=open(
            'media/toronto.jpg', 'rb').read(), content_type='image/jpeg')

        self.extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(9.99), 2),
            image=self.image.name,
        )

    def test_get_extras_page(self):
        """
        Verifies that a status of 200 is returned and the extras template was
        used when the user tries to access the extras page
        """
        response = self.client.get('/extras/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extras/extras.html')

    def test_standard_user_get_add_extra_page(self):
        """
        Logs in the standard user and verifies that a status of 403 is returned
        when they try and access the add extra page. Code for the login is
        from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/extras/add/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_get_add_extra_page(self):
        """
        Logs in the superuser and verifies that a status of 200 is returned and
        the add extra template was used when they try and access the add
        extra page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.get('/extras/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extras/add_extra.html')

    def test_can_add_extra(self):
        """
        Logs in the superuser and verifies that they are redirected to the
        extras page and a new extra is created in the database when a post
        request with valid extra details is submitted to the add extra page.
        Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.post('/extras/add/', {
            'name': 'Test Extra 2',
            'description': 'Test Description',
            'price': '4.99',
            'image':  self.image}, enctype="multipart/form-data")
        self.assertRedirects(response, '/extras/')
        extra = Extra.objects.filter(name='Test Extra 2')
        self.assertEqual(len(extra), 1)

    def test_standard_user_get_edit_extra_page(self):
        """
        Logs in the standard user and verifies that a status of 403 is returned
        when they try and access the edit extra page. Code for the login is
        from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(f'/extras/edit/{self.extra.slug}/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_get_edit_extra_page(self):
        """
        Logs in the superuser and verifies that a status of 200 is returned and
        the edit extra template was used when they try and access the edit
        extra page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.get(f'/extras/edit/{self.extra.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extras/edit_extra.html')

    def test_can_edit_extra(self):
        """
        Logs in the superuser and verifies that they are redirected to the
        extras page and updates the extra's price in the database when
        a post request with valid extra details is submitted to the edit extra
        page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.post(f'/extras/edit/{self.extra.slug}/', {
            'name': 'Test Extra',
            'description': 'Test Description',
            'price': '9.99',
            'image':  self.image.name}, enctype="multipart/form-data")
        self.assertRedirects(response, '/extras/')
        extra = Extra.objects.get(name='Test Extra')
        self.assertEqual(extra.price, round(Decimal(9.99), 2))

    def test_standard_user_can_delete_extra(self):
        """
        Logs in the standard user and verifies that a status of 403 is returned
        when they try and access the delete extra page. Code for the login is
        from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(f'/extras/delete/{self.extra.slug}/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_delete_extra(self):
        """
        Logs in the superuser and verifies that they are redirected to the
        extras page and deletes the extra from the database.
        Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.get(f'/extras/delete/{self.extra.slug}/')
        self.assertRedirects(response, '/extras/')
        extra = Extra.objects.filter(name='Test Extra')
        self.assertEqual(len(extra), 0)


class TestExtrasForm(TestCase):
    def test_required_form_fields(self):
        """Tests the required fields in the extra form"""
        form = ExtraForm({
            'name': '',
            'description': '',
            'price': '',
            'image': '',
        })
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertEqual(form.errors['description']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['price'][0], 'This field is required.')
        self.assertEqual(form.errors['image'][0], 'This field is required.')

    def test_invalid_form_field_inputs(self):
        """Tests invalid inputs in the extra form"""
        form = ExtraForm({
            'name': 'Test Extra',
            'description': 'Test Description',
            'price': 'A price',
            'image': 'test_image.jpg'
        })
        self.assertEqual(form.errors['price'][0], 'Enter a number.')

    def test_excluded_in_form_metaclass(self):
        """Tests the excluded attribute of the extra form meta class"""
        form = ExtraForm()
        self.assertEqual(form.Meta.exclude, ('image_url',))


class TestExtrasModels(TestCase):
    def test_extra_string_method(self):
        """
        Creates an extra and verifies that the string
        method is correct
        """
        extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(4.99), 2),
            image='testimage.jpg',
        )
        self.assertEqual(str(extra), 'Test Extra - £4.99')
