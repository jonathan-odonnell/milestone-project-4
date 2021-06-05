from django.test import TestCase
from .models import Package
from .forms import (PackageForm, FeatureForm, FeatureFormset, ActivityForm,
                    ActivityFormset, ItineraryForm, ItineraryFormset, ReviewForm)


class TestHolidayForms(TestCase):
    def setUp(self):
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

    def test_feature_formset_all_fields_not_required(self):
        form = FeatureFormset({
            'features-TOTAL_FORMS': '1',
            'features-INITIAL_FORMS': '0',
            'features-MIN_NUM_FORMS': '0',
            'features-MAX_NUM_FORMS': '5',
            'features-0-name': '',
            'features-0-DELETE': '',
        }, instance=self.holiday)
        self.assertTrue(form.is_valid())

    def test_activity_formset_all_fields_not_required(self):
        form = ActivityFormset({
            'activities-TOTAL_FORMS': '1',
            'activities-INITIAL_FORMS': '0',
            'activities-MIN_NUM_FORMS': '0',
            'activities-MAX_NUM_FORMS': '1000',
            'activities-0-name': '',
            'activities-0-description': '',
        }, instance=self.holiday)
        self.assertTrue(form.is_valid())

    def test_itinerary_formset_all_fields_not_required(self):
        form = ItineraryFormset({
            'itineraries-TOTAL_FORMS': '1',
            'itineraries-INITIAL_FORMS': '0',
            'itineraries-MIN_NUM_FORMS': '0',
            'itineraries-MAX_NUM_FORMS': '1000',
            'itineraries-0-day': '',
            'itineraries-0-name': '',
            'itineraries-0-description': '',
        }, instance=self.holiday)
        self.assertTrue(form.is_valid())

    def test_review_form_all_fields_required(self):
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

    def test_exclude_in_package_form_metaclass(self):
        form = PackageForm()
        self.assertEqual(form.Meta.exclude, ('rating',))

    def test_fields_in_feature_form_metaclass(self):
        form = FeatureForm()
        self.assertEqual(form.Meta.fields, '__all__')

    def test_fields_in_activity_form_metaclass(self):
        form = ActivityForm()
        self.assertEqual(form.Meta.fields, '__all__')

    def test_fields_in_itinerary_form_metaclass(self):
        form = ItineraryForm()
        self.assertEqual(form.Meta.fields, '__all__')

    def test_exclude_in_review_form_metaclass(self):
        form = ReviewForm()
        self.assertEqual(form.Meta.exclude, ('date',))
