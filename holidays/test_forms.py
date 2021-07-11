from django.test import TestCase
from .models import Package
from .forms import (PackageForm, FeatureForm, FeaturesFormSet, ActivityForm,
                    ActivitiesFormSet, ItineraryForm, ItinerariesFormSet,
                    ReviewForm)


class TestHolidayForms(TestCase):
    def setUp(self):
        """Sets up the package"""
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

    def test_package_form_required_fields(self):
        """Tests the required fields in the package form"""
        form = PackageForm({
            'name': '',
            'image': '',
            'description': '',
            'price': '',
            'catering': '',
        })
        self.assertEqual(form.errors['name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['image'][0], 'This field is required.')
        self.assertEqual(form.errors['description']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['price']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['catering']
                         [0], 'This field is required.')

    def test_package_form_invalid_price_input(self):
        """Tests invalid price input in the package form"""
        form = PackageForm({
            'name': 'Test',
            'image': 'test.jpg',
            'description': 'Test',
            'price': 'Not a price',
            'catering': 'Test',
        })
        self.assertEqual(form.errors['price']
                         [0], 'Enter a number.')

    def test_package_form_exclude_in_metaclass(self):
        """Tests the excluded attribute of the package form meta class"""
        form = PackageForm()
        self.assertEqual(form.Meta.exclude, ('rating', 'image_url'))

    def test_features_formset_all_fields_not_required(self):
        """Tests the required fields in the features formset"""
        form = FeaturesFormSet({
            'features-TOTAL_FORMS': '1',
            'features-INITIAL_FORMS': '0',
            'features-MIN_NUM_FORMS': '0',
            'features-MAX_NUM_FORMS': '5',
            'features-0-name': '',
            'features-0-DELETE': '',
        }, instance=self.holiday)
        self.assertTrue(form.is_valid())

    def test_feature_form_fields_in_metaclass(self):
        """Tests the all attribute of the feature form meta class"""
        form = FeatureForm()
        self.assertEqual(form.Meta.fields, '__all__')

    def test_activities_formset_all_fields_not_required(self):
        """Tests the required fields in the activities formset"""
        form = ActivitiesFormSet({
            'activities-TOTAL_FORMS': '1',
            'activities-INITIAL_FORMS': '0',
            'activities-MIN_NUM_FORMS': '0',
            'activities-MAX_NUM_FORMS': '1000',
            'activities-0-name': '',
            'activities-0-description': '',
        }, instance=self.holiday)
        self.assertTrue(form.is_valid())

    def test_activity_form_fields_in_metaclass(self):
        """Tests the all attribute of the activity form meta class"""
        form = ActivityForm()
        self.assertEqual(form.Meta.fields, '__all__')

    def test_itineraries_formset_all_fields_not_required(self):
        """ Tests the required fields in the itineraries formset """
        form = ItinerariesFormSet({
            'itineraries-TOTAL_FORMS': '1',
            'itineraries-INITIAL_FORMS': '0',
            'itineraries-MIN_NUM_FORMS': '0',
            'itineraries-MAX_NUM_FORMS': '1000',
            'itineraries-0-day': '',
            'itineraries-0-name': '',
            'itineraries-0-description': '',
        }, instance=self.holiday)
        self.assertTrue(form.is_valid())

    def test_itinerary_form_fields_in_metaclass(self):
        """Tests the all attribute of the itinerary form meta class"""
        form = ItineraryForm()
        self.assertEqual(form.Meta.fields, '__all__')

    def test_review_form_all_fields_required(self):
        """Tests the required fields in the review form"""
        form = ReviewForm({
            'package': '',
            'full_name': '',
            'rating': '',
            'title': '',
            'review': ''
        })
        self.assertEqual(form.errors['package']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['full_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['rating']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['title']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['review']
                         [0], 'This field is required.')

    def test_review_form_exclude_in_metaclass(self):
        """Tests the excluded attribute of the review form meta class"""
        form = ReviewForm()
        self.assertEqual(form.Meta.exclude, ('date',))
