from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import create_bitmask
from locationstore.models import Film

import json

@csrf_exempt
def get_films(request):
    """
    This function returns a mask in the format [1, 1, 0, 1, 0, 0...] that tells us which movies should be shown. We sort
    all movies in the database by title on each query and when we dump the JSON used by Javascript, meaning that we can 
    rely on the mask referring to the same elements on both the client and server.
    """
    query = request.GET.get('q', '')

    if query:
        all_films = Film.objects.filter().order_by('title')
        bitmask = create_bitmask(films=list(all_films.filter(Q(title__icontains=query) | Q(release_year__icontains=query)).order_by('title')), all_films=list(all_films))
    else:
        bitmask = [1] * len(Film.objects.filter().count())

    return HttpResponse(json.dumps(bitmask), content_type="application/json")
