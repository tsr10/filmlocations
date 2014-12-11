def get_autocomplete_text(films):
    """
    Creates the autocomplete text from a queryset of films.
    """
    response_text = []
    for film in films:
        location = " location" if len(film.location) == 1 else " locations"
        response_text.append({
            'title' : film.title,
            'location' : "Shot in " + str(len(film.location)) + location + " in San Francisco",
            'release_year' : film.release_year,
        })
    return response_text