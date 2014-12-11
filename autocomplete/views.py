from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import get_autocomplete_text
from locationstore.models import Film

import json

@csrf_exempt
def autocomplete(request):
    """
    The autocomplete function that gets called when a user types into the search box. When filtering the film objects
    in the database, we need to filter out null locations and locations that were improperly geocoded. This function returns
    a json object of the first 5 films found that match the query.
    """
    query = request.GET.get('q', '')

    films = Film.objects.filter(Q(title__icontains=query) | Q(release_year__icontains=query), ~Q(location=[]))[:5]

    response_text = get_autocomplete_text(films)

    return HttpResponse(json.dumps(response_text), content_type="application/json")
