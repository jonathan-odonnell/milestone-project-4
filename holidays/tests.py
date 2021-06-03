from django.test import TestCase
from .models import Region, Category, Country, Package
from io import BytesIO
from decimal import Decimal
from datetime import datetime
from pytz import timezone
import pytz

class TestHolidaysViews(TestCase):
    def setUp(self):
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
        """
        Code for adding the flights related object is from 
        https://docs.djangoproject.com/en/3.2/ref/models/relations/
        """
        self.holiday.flights.create(
            flight_number='ZZ001',
            origin='Test Airport',
            destination='Test Airport',
            departure_time=datetime(2021, 6, 1, tzinfo=pytz.utc),
            origin_time_zone=timezone('Europe/London'),
            arrival_time=datetime(2021, 6, 2, tzinfo=pytz.utc),
            destination_time_zone=timezone('Europe/London'),
            baggage=Decimal(20)
        )

    def test_get_holiday_category_page(self):
        response = self.client.get('/holidays/city-breaks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_holiday_destination_page(self):
        response = self.client.get('/holidays/destinations/north-america/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_offers_page(self):
        response = self.client.get('/holidays/offers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_sorted_holiday_destination_page(self):
        response = self.client.get('/holidays/destinations/north-america/?sort=price&direction=asc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_filtered_countries_holiday_destination_page(self):
        response = self.client.get(f'/holidays/destinations/north-america/?countries=usa')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_filtered_categories_holiday_destination_page(self):
        response = self.client.get('/holidays/destinations/north-america/?categories=city-breaks')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holidays.html')

    def test_get_holiday_category_details_page(self):
        response = self.client.get('/holidays/city-breaks/test-holiday/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_get_holiday_destination_details_page(self):
        response = self.client.get('/holidays/destinations/north-america/test-holiday/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holidays/holiday_details.html')

    def test_booking_form_submit(self):
        response = self.client.post(f'/booking/{self.holiday.id}', {
            'departure_date': '01/06/2021',
            'departure_airport': 'Test Airport',
            'guests': '2'
        })
        self.assertRedirects
        (response, '/booking/')

