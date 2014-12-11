from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand

from locationstore.models import Film

import json
import requests
import time

class Command(BaseCommand):
    """
    Loads the latLngs into the DB. We throw away results that lie outside San Francisco and results that don't 
    match anything. If a film has no valid locations, we delete the film from the DB. This function is idempotent,
    but only updates locations without longitudes and latitudes. At the end of this function, we dump the results 
    to allFilms.json.
    """
    help = 'Loads in the lat/longs'

    def handle(self, *args, **options):
        for film in Film.objects.filter():
            location_list = []
            for location, latitude, longitude in film.location:
                if latitude == "" and longitude == "":
                    address = location.replace(' ', '+')
                    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address + ',+San+Francisco,+CA&key=AIzaSyAbS1T8qqWepAclNqOHMK_WC7tyea9sN5I')
                    r_dict = json.loads(r.text)
                    if r_dict['status'] == 'OK':
                        latitude = r_dict['results'][0]['geometry']['location']['lat']
                        longitude = r_dict['results'][0]['geometry']['location']['lng']
                        if ((float(latitude) < 37.85) & (float(latitude) > 37.75) & (float(longitude) > -122.5) & (float(longitude) < -122.3)):
                            if (str(latitude) != "37.7749295") | (str(longitude) != "-122.4194155"):
                                location_list.append([location, latitude, longitude])
                    #Only five requests per second are allowed
                    time.sleep(.25)
                else:
                    location_list.append([location, latitude, longitude])
            if location_list:
                film.location = location_list
                film.save()
            else:
                film.delete()

        data = serializers.serialize("json", Film.objects.filter().order_by('title'), fields=('title', 'location'), indent=4)
        data_output = open(settings.BASE_DIR + '/static/js/allfilms.json', 'w')
        data_output.write("allFilms = " + data)