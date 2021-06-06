from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from .models import Region, Category, Country, Package, Review
from booking.models import Booking
from datetime import date


class TestHolidaysViews(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Password',
            first_name='Test',
            last_name='Admin'
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password',
            first_name='Test',
            last_name='User'
        )

        EmailAddress.objects.create(
            user=self.superuser,
            email=self.superuser.email
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

        # https://stackoverflow.com/questions/29721360/django-test-with-allauth
        current_site = Site.objects.get_current()

        current_site.socialapp_set.create(
            provider="facebook",
            name="facebook",
            client_id="1234567890",
            secret="0987654321",
        )

        current_site.socialapp_set.create(
            provider="google",
            name="google",
            client_id="1234567890",
            secret="0987654321",
        )

        # https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
        self.image = SimpleUploadedFile(name='test_image.jpg', content=open(
            'media/toronto.jpg', 'rb').read(), content_type='image/jpeg')

        category = Category.objects.create(
            name="City Breaks",
            page_title="City Breaks",
            image=self.image.name
        )
        self.region = Region.objects.create(
            name="North America",
            page_title="North America",
            image=self.image.name
        )
        country = Country.objects.create(
            name='USA'
        )
        self.holiday = Package.objects.create(
            country=country,
            region=self.region,
            category=category,
            name='Test Holiday',
            image=self.image.name,
            description='Test description',
            offer=True,
            price=499,
            duration=14,
            catering='Full Board',
            transfers_included=True
        )

    def test_get_holiday_category_page(self):
        response = self.client.get(f'/holidays/{self.holiday.category.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_holiday_destination_page(self):
        response = self.client.get(
            f'/holidays/destinations/{self.holiday.region.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_holiday_offers_page(self):
        response = self.client.get('/holidays/offers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_sorted_holiday_destination_page(self):
        # https://stackoverflow.com/questions/4794457/unit-testing-django-json-view
        response = self.client.get(
            f'/holidays/destinations/{self.holiday.region.slug}/?sort=price&direction=asc', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'holidays/includes/holiday_cards.html')

    def test_get_filtered_countries_holiday_category_page(self):
        # https://stackoverflow.com/questions/4794457/unit-testing-django-json-view
        response = self.client.get(
            f'/holidays/{self.holiday.category.slug}/?countries=usa', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'holidays/includes/holiday_cards.html')

    def test_get_filtered_categories_holiday_destination_page(self):
        # https://stackoverflow.com/questions/4794457/unit-testing-django-json-view
        response = self.client.get(
            f'/holidays/destinations/{self.holiday.region.slug}/?categories=city-breaks', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'holidays/includes/holiday_cards.html')

    def test_get_holiday_category_details_page(self):
        response = self.client.get(
            f'/holidays/{self.holiday.category.slug}/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_get_holiday_offers_details_page(self):
        response = self.client.get(f'/holidays/offers/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_get_holiday_destination_details_page(self):
        response = self.client.get(
            f'/holidays/destinations/{self.holiday.region.slug}/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_anonymous_user_get_reviews_page(self):
        response = self.client.get(f'/holidays/review/{self.holiday.slug}/')
        self.assertRedirects(
            response, f'/accounts/login/?next=/holidays/review/{self.holiday.slug}/')

    def test_logged_in_user_with_booking_get_reviews_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )

        Booking.objects.create(
            user_profile=self.user.userprofile,
            package=self.holiday,
            guests=1,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            paid=True
        )
        response = self.client.get(f'/holidays/review/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/review.html')

    def test_logged_in_user_without_booking_get_reviews_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(f'/holidays/review/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 403)

    def test_reviews_form_submit(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )

        Booking.objects.create(
            user_profile=self.user.userprofile,
            package=self.holiday,
            guests=1,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            paid=True
        )

        response = self.client.post(f'/holidays/review/{self.holiday.slug}/', {
            'rating': '5',
            'title': 'Test Title',
            'review': 'Test Review'
        })

        self.assertRedirects(
            response, f'/holidays/destinations/{self.holiday.region.slug}/{self.holiday.slug}/')
        review = Review.objects.filter(
            full_name=self.user.get_full_name(), package=self.holiday)
        self.assertEqual(len(review), 1)

    def test_standard_user_get_add_holiday_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/holidays/add/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_get_add_holiday_page(self):
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.get('/holidays/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/add_holiday.html')

    def test_can_add_holiday(self):
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.post('/holidays/add/', {
            'region': self.region.id,
            'name': 'Test holiday 1',
            'image': self.image,
            'description': 'Test description',
            'price': '499.00',
            'duration': '7',
            'catering': 'Test catering type',
            'transfers_included': 'on',
            'features-TOTAL_FORMS': '1',
            'features-INITIAL_FORMS': '0',
            'features-MIN_NUM_FORMS': '0',
            'features-MAX_NUM_FORMS': '5',
            'features-0-name': '',
            'activities-TOTAL_FORMS': '1',
            'activities-INITIAL_FORMS': '0',
            'activities-MIN_NUM_FORMS': '0',
            'activities-MAX_NUM_FORMS': '1000',
            'activities-0-name': '',
            'activities-0-description': '',
            'itineraries-TOTAL_FORMS': '1',
            'itineraries-INITIAL_FORMS': '0',
            'itineraries-MIN_NUM_FORMS': '0',
            'itineraries-MAX_NUM_FORMS': '1000',
            'itineraries-0-day': '',
            'itineraries-0-title': '',
            'itineraries-0-description': '',
        }, enctype='multipart/form-data')
        holiday = Package.objects.filter(name='Test holiday 1')
        self.assertEqual(len(holiday), 1)
        self.assertRedirects(
            response, f'/holidays/destinations/{holiday.first().region.slug}/{holiday.first().slug}/')

    def test_standard_user_get_edit_holiday_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(f'/holidays/edit/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_get_edit_holiday_page(self):
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.get(f'/holidays/edit/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/edit_holiday.html')

    def test_can_edit_holiday(self):
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        holiday = Package.objects.create(
            region=self.region,
            name='Test holiday 2',
            image='test.jpg',
            description='Test description',
            offer=False,
            price='599.00',
            duration=7,
            catering='Test catering type',
            transfers_included=True,
        )
        response = self.client.post(f'/holidays/edit/{holiday.slug}/', {
            'region': self.region.id,
            'name': 'Test holiday 2',
            'image': self.image,
            'description': 'Test description',
            'price': '599.00',
            'duration': '7',
            'catering': 'Test catering type',
            'transfers_included': 'on',
            'features-TOTAL_FORMS': '1',
            'features-INITIAL_FORMS': '0',
            'features-MIN_NUM_FORMS': '0',
            'features-MAX_NUM_FORMS': '5',
            'features-0-name': '',
            'activities-TOTAL_FORMS': '1',
            'activities-INITIAL_FORMS': '0',
            'activities-MIN_NUM_FORMS': '0',
            'activities-MAX_NUM_FORMS': '1000',
            'activities-0-name': '',
            'activities-0-description': '',
            'itineraries-TOTAL_FORMS': '1',
            'itineraries-INITIAL_FORMS': '0',
            'itineraries-MIN_NUM_FORMS': '0',
            'itineraries-MAX_NUM_FORMS': '1000',
            'itineraries-0-day': '',
            'itineraries-0-title': '',
            'itineraries-0-description': '',
        }, enctype='multipart/form-data')
        holiday = Package.objects.get(id=holiday.id)
        self.assertEqual(holiday.price, 599)
        self.assertRedirects(
            response, f'/holidays/destinations/{holiday.region.slug}/{holiday.slug}/')

    def test_standard_user_cant_delete_holiday(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(f'/holidays/delete/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_delete_holiday(self):
        self.client.login(
            email=self.superuser.email,
            password='Password',
        )
        response = self.client.get(f'/holidays/delete/{self.holiday.slug}/')
        self.assertRedirects(response, '/')
        holiday = Package.objects.filter(id=self.holiday.id)
        self.assertEqual(len(holiday), 0)
