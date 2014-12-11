"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from autocomplete.utils import get_autocomplete_text
from locationstore.models import Film
from map.utils import create_bitmask


class GetAutocompleteTextTest(TestCase):
    """
    Tests the get_autocomplete_text function.
    """
    def setUp(self):
        self.film_info = [Film(title='title_1',
                        location='location_1',
                        release_year='release_year_1'),
                        Film(title='title_2',
                        location='location_2',
                        release_year='release_year_2'),
                        Film(title='title_3',
                        location='location_3',
                        release_year='release_year_3'),
                        Film(title='title_4',
                        location='location_4',
                        release_year='release_year_4'),
                        Film(title='title_5',
                        location='location_5',
                        release_year='release_year_5'),]

    def test_get_autocomplete_text(self):
        response_text = get_autocomplete_text(films=self.film_info)
        self.assertEqual(response_text, [{'release_year': 'release_year_1', 'location': 'Shot in 10 locations in San Francisco', 'title': 'title_1'}, {'release_year': 'release_year_2', 'location': 'Shot in 10 locations in San Francisco', 'title': 'title_2'}, {'release_year': 'release_year_3', 'location': 'Shot in 10 locations in San Francisco', 'title': 'title_3'}, {'release_year': 'release_year_4', 'location': 'Shot in 10 locations in San Francisco', 'title': 'title_4'}, {'release_year': 'release_year_5', 'location': 'Shot in 10 locations in San Francisco', 'title': 'title_5'}])

class CreateBitmaskTest(TestCase):
    """
    Tests the create_bitmask function.
    """
    def setUp(self):
        self.film_1 = Film(pk=1,
                        title='title_1',
                        location='location_1',
                        release_year='release_year_1')
        self.film_2 = Film(pk=2,
                        title='title_2',
                        location='location_2',
                        release_year='release_year_2')
        self.film_3 = Film(pk=3,
                        title='title_3',
                        location='location_3',
                        release_year='release_year_3')
        self.film_4 = Film(pk=4,
                        title='title_4',
                        location='location_4',
                        release_year='release_year_4')
        self.film_5 = Film(pk=5,
                        title='title_5',
                        location='location_5',
                        release_year='release_year_5')
        self.film_info = [self.film_1, self.film_2, self.film_3, self.film_4, self.film_5]

    def test_get_autocomplete_text_blank_query(self):
        bitmask = create_bitmask(films=[], all_films=self.film_info)
        self.assertEqual(bitmask, [0, 0, 0, 0, 0])

    def test_get_autocomplete_text_full_query(self):
        films = [self.film_1, self.film_2, self.film_3, self.film_4, self.film_5]
        bitmask = create_bitmask(films=films, all_films=self.film_info)
        self.assertEqual(bitmask, [1, 1, 1, 1, 1])

    def test_get_autocomplete_text_partial_query(self):
        films = [self.film_3, self.film_4]
        bitmask = create_bitmask(films=films, all_films=self.film_info)
        self.assertEqual(bitmask, [0, 0, 1, 1, 0])
