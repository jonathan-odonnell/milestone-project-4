from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import Extra
from .forms import ExtraForm
from decimal import Decimal


class TestExtrasViews(TestCase):
    def setUp(self):

        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=user,
            email='admin@example.com',
        )

        self.client.login(
            email='admin@example.com',
            password='Password',
        )

        # https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
        self.image = SimpleUploadedFile(name='test_image.jpg', content=open('media/toronto.jpg', 'rb').read(), content_type='image/jpeg')

    def test_get_extras_page(self):
        response = self.client.get('/extras/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extras/extras.html')

    def test_get_add_extra_page(self):
        response = self.client.get('/extras/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extras/add_extra.html')


    def test_can_add_extra(self):
        response = self.client.post('/extras/add/', {
            'name': 'Test Extra',
            'description': 'Test Description',
            'price': '4.99',
            'image':  self.image}, enctype="multipart/form-data")
        self.assertRedirects(response, '/extras/')
        extra = Extra.objects.filter(name='Test Extra')
        self.assertEqual(len(extra), 1)

    def test_get_edit_extra_page(self):
        extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(9.99), 2),
            image=self.image.name,
        )
        response = self.client.get(f'/extras/edit/{extra.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extras/edit_extra.html')


    def test_can_edit_extra(self):
        extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(4.99), 2),
            image=self.image.name,
        )
        response = self.client.post(f'/extras/edit/{extra.id}/', {
            'name': 'Test Extra',
            'description': 'Test Description',
            'price': '9.99',
            'image':  self.image.name}, enctype="multipart/form-data")
        self.assertRedirects(response, '/extras/')
        extra = Extra.objects.get(name='Test Extra')
        self.assertEqual(extra.price, round(Decimal(9.99), 2))


    def test_delete_extra_link(self):
        extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(4.99), 2),
            image=self.image.name,
        )
        response = self.client.get(f'/extras/delete/{extra.id}/')
        self.assertRedirects(response, '/extras/')
        extra = Extra.objects.filter(name='Test Extra')
        self.assertEqual(len(extra), 0)


class TestExtrasForm(TestCase):
    def test_required_form_fields(self):
        form = ExtraForm({
            'name': '',
            'description': '',
            'price': '',
            'image': '',
        })
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertEqual(form.errors['description'][0], 'This field is required.')
        self.assertEqual(form.errors['price'][0], 'This field is required.')
        self.assertEqual(form.errors['image'][0], 'This field is required.')


    def test_invalid_form_field_input(self):
        form = ExtraForm({
            'name': 'Test Extra',
            'description': 'Test Description',
            'price': 'A price',
            'image': 'test_image.jpg'
        })
        self.assertEqual(form.errors['price'][0], 'Enter a number.')
        

    def test_excluded_in_form_metaclass(self):
        form = ExtraForm()
        self.assertEqual(form.Meta.exclude, ('image_url',))


class TestExtrasModels(TestCase):
    def test_string_method_returns_extra_name(self):
        extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(4.99), 2),
            image='testimage.jpg',
        )
        self.assertEqual(str(extra), f'Test Extra - £4.99')        
      