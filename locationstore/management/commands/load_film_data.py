from django.conf import settings
from django.core.management.base import BaseCommand

from locationstore.models import Film

import csv


class Command(BaseCommand):
    """
    Loads in the film data. We only use title, release_year, and address. Adding new fields would be easy
    if we wanted to add them. This function is idempotent, but you must also run find_lat_long afterwards
    before using the site.
    """
    help = 'Loads in the film data'

    def handle(self, *args, **options):
        with open(settings.BASE_DIR + '/locationstore/sffilmlocations.csv', 'rU') as f:
            reader = csv.reader(f, dialect=csv.excel)
            next(reader, None)
            for row in reader:
                row = [unicode(cell, 'utf-8') for cell in row]
                film, created = Film.objects.get_or_create(
                    title=row[0],
                    release_year=row[1],
                    )
                film.location.extend([(row[2], "", "")])
                film.save()