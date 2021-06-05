from django.test import TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import Region, Category, Country, Package, Review
from booking.models import Booking
from io import BytesIO
from decimal import Decimal
from datetime import date

class TestHolidaysViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='test',
            email='test@example.com',
            password='Password',
            first_name='Test',
            last_name='User',
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

        self.client.login(
            email=self.user.email,
            password='Password',
        )

        img = BytesIO(b'testimage')
        img.name = 'testimage.jpg'
        category = Category.objects.create(
            name="City Breaks", 
            page_title="City Breaks", 
            image=img.name
        )
        region = Region.objects.create(
            name="North America", 
            page_title="North America", 
            image=img.name
        )
        country = Country.objects.create(
            name = 'USA'
        )
        self.holiday = Package.objects.create(
            country = country,
            region = region,
            category = category,
            name='Test Holiday',
            image=img.name,
            description='Test description',
            offer=True,
            price=Decimal(499),
            duration=Decimal(14),
            catering='Full Board',
            transfers_included=True
        )

        self.booking = Booking.objects.create(
            user_profile=self.user.userprofile,
            package=self.holiday,
            guests=1,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            paid=True,
        )

    def test_get_holiday_category_page(self):
        response = self.client.get(f'/holidays/{self.holiday.category.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_holiday_destination_page(self):
        response = self.client.get(f'/holidays/destinations/{self.holiday.region.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_offers_page(self):
        response = self.client.get('/holidays/offers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_sorted_holiday_destination_page(self):
        response = self.client.get(f'/holidays/destinations/{self.holiday.region.slug}/?sort=price&direction=asc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_filtered_countries_holiday_category_page(self):
        response = self.client.get(f'/holidays/{self.holiday.category.slug}/?countries=usa')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_filtered_categories_holiday_destination_page(self):
        response = self.client.get(f'/holidays/destinations/{self.holiday.region.slug}/?categories=city-breaks')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_holiday_category_details_page(self):
        response = self.client.get(f'/holidays/{self.holiday.category.slug}/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_get_holiday_destination_details_page(self):
        response = self.client.get(f'/holidays/destinations/{self.holiday.region.slug}/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_get_reviews_page(self):
        response = self.client.get(f'/holidays/review/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/review.html')

    def test_reviews_form_submit(self):
        response = self.client.post(f'/holidays/review/{self.holiday.slug}/', {
            'rating': '5',
            'title': 'Test Title',
            'review': 'Test Review'
        })
        self.assertRedirects(response, f'/holidays/destinations/{self.holiday.region.slug}/{self.holiday.slug}/')
        review = Review.objects.filter(full_name=self.user.get_full_name(), package=self.holiday)
        self.assertEqual(len(review), 1)

    def test_get_add_holiday_page(self):
        response = self.client.get('/holidays/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/add_holiday.html')

    def test_get_edit_holiday_page(self):
        response = self.client.get(f'/holidays/edit/{self.holiday.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/edit_holiday.html')

    def test_can_delete_holiday(self):
        holiday = self.holiday = Package.objects.create(
            name='Test Holiday 2',
            image='test_image.jpg',
            description='Test description',
            offer=True,
            price=499,
            duration=14,
            catering='Full Board',
            transfers_included=True
        )
        response = self.client.get(f'/holidays/delete/{holiday.slug}/')
        self.assertRedirects(response,'/')
        holiday = Package.objects.filter(id=holiday.id)
        self.assertEqual(len(holiday), 0)
