from django.test import TestCase
from django.contrib.auth.models import User
from .models import(Category, Region, Country, Package,
                    Feature, Activity, Itinerary, Review)


class TestHolidaysModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='test',
            email='test@example.com',
            password='Password',
            first_name='Test',
            last_name='User',
        )
       
        self.holiday = Package.objects.create(
            name='Test Holiday',
            image='test_image.jpg',
            description='Test description',
            offer=True,
            price=499,
            duration=14,
            catering='Full Board',
            transfers_included=True
        )

    def test_category_string_method(self):
        category = Category.objects.create(
            name="City Breaks",
            page_title="City Breaks",
            image='test_image.jpg'
        )
        self.assertEqual(str(category), category.name)

    def test_region_string_method(self):
        region = Region.objects.create(
            name="North America",
            page_title="North America",
            image='test_image.jpg'
        )
        self.assertEqual(str(region), region.name)

    def test_country_string_method(self):
        country = Country.objects.create(
            name='USA'
        )
        self.assertEqual(str(country), country.name)

    def test_package_string_method(self):
        self.assertEqual(str(self.holiday), self.holiday.name)

    def test_package_rating_default(self):
        self.assertEqual(self.holiday.rating, 0)

    def test_feature_string_method(self):
        feature = Feature.objects.create(
            package=self.holiday,
            name='Test Feature'
        )
        self.assertEqual(str(feature), feature.name)

    def test_activity_string_method(self):
        activity = Activity.objects.create(
            package=self.holiday,
            name='Test Activity',
            description='Test Description'
        )
        self.assertEqual(str(activity), activity.name)

    def test_itinerary_string_method(self):
        itinerary = Itinerary.objects.create(
            package=self.holiday,
            day='Day 1',
            name='Test Itinerary',
            description='Test Description'
        )
        self.assertEqual(str(itinerary), itinerary.name)

    def test_review_string_method(self):
        review = Review.objects.create(
            package=self.holiday,
            full_name=self.user.get_full_name(),
            rating=5,
            title='Test Title',
            review='Test Review'
        )
        self.assertEqual(str(review), review.title)
