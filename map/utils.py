def create_bitmask(films, all_films):
    """
    Creates the bitmask off of a query and all the films in the DB. The films are fetched from the DB in 
    map/views.py.
    """
    bitmask = []
    
    while len(films) > 0:
        if all_films[0] == films[0]:
            bitmask.append(1)
            films.pop(0)
            all_films.pop(0)
        else:
            bitmask.append(0)
            all_films.pop(0)
    bitmask += [0] * (len(all_films) - len(films))

    return bitmask