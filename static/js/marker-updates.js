///The global variables. We check against these before deciding whether or not to perform an
///update. Updates are costly. This maintains the state of the application, so to simplify things I try to hit
///these variables as little as possible.

/*jslint nomen: true */
/*global google: false, _: false, $: false, Handlebars: false */
"use strict";

var FILMLOCATIONS = {};
FILMLOCATIONS.canUpdateData = true;
FILMLOCATIONS.canUpdateMarkers = true;
FILMLOCATIONS.markers = [];
FILMLOCATIONS.updateOrder = 1;
FILMLOCATIONS.nextQuery = {'query' : "",
                              'refocus' : true};

function makeLatLng(location) {
    var latLng = new google.maps.LatLng(location[1], location[2]);
    return latLng;
}

function buildLatLngList(film) {
    var latLngList = _.map(film.fields.location, makeLatLng);
    return latLngList;
}

///This function builds the initial latLngLists that we generate the markers off of.
function buildLatLngLists(films) {
    var latLngLists = _.map(films, buildLatLngList);
    return latLngLists;
}

function makeMarker(map, latLng) {
    var marker = new google.maps.Marker({
        position: latLng,
        map: map,
    });
    return marker;
}

function makeMarkerList(map, latLngList) {
    var markerList = _.map(latLngList, _.partial(makeMarker, map));
    return markerList;
}

///Creates the markers. Calls the helper function makeMarkers, where the markers are actually
///generated.
function createMarkerLists(map, latLngLists) {
    var markerLists = _.map(latLngLists, _.partial(makeMarkerList, map));
    return markerLists;
}

///Resizes the map according to the passed bounds variable. We scroll up by 50 in order to account to the screen
///real estate taken up by the search bar.
function resizeMap(bounds, map) {
    map.fitBounds(bounds);
    if (map.getZoom() > 15) {
        map.setZoom(15);
    }
    map.panBy(0, -50);
}

///Creates an array completely initialized to a specific value (in our case, 1). Creates the initial mask that
///indicates that we want to see all markers.
function fillArray(value, len) {
    var arr = [],
        i;
    for (i = 0; i < len; i = i + 1) {
        arr.push(value);
    }
    return arr;
}

//Creates our initial map. Called upon page load in index.html.
function initializeFilmLocations(markerLists) {
    var numberOfMarkers = markerLists.length,
        mostRecentUpdate = {'counter' : 0,
                            'mask' : fillArray(1, numberOfMarkers),
                            'refocus' : true},
        oldMask = fillArray(1, numberOfMarkers),
        markers = markerLists;
    return {'numberOfMarkers' : numberOfMarkers,
            'mostRecentUpdate' : mostRecentUpdate,
            'oldMask' : oldMask,
            'markers' : markers};
}

function extendBounds(markerList, bounds) {
    _.each(markerList, function (marker) { bounds.extend(marker.getPosition()); });
    return bounds;
}

///Resizes the map according to the new co-ordinates. We only run this when either an empty query
///is sent or a film is clicked on.
function extendMarkerListsBounds(markerLists, bounds) {
    markerLists.forEach(function (markerList) {
        bounds = extendBounds(markerList, bounds);
    });
    return bounds;
}

function makeInfoWindow(map, infoWindowContent, locationMarker) {
    var infoWindow = new google.maps.InfoWindow({
        content: infoWindowContent(locationMarker[0])
    });
    infoWindow.marker = locationMarker[1];
    google.maps.event.addListener(locationMarker[1], 'click', function () {
        infoWindow.open(map, locationMarker[1]);
        if (FILMLOCATIONS.lastWindow !== undefined) {
            FILMLOCATIONS.lastWindow.close();
        }
        FILMLOCATIONS.lastWindow = infoWindow;
    });
    return infoWindow;
}

function makeInfoWindows(map, filmMarkerList) {
    var infoWindowContent = Handlebars.compile("<b>" + filmMarkerList[0].fields.title + "</b><br>{{[0]}}"),
        locationList = filmMarkerList[0].fields.location,
        markerList = filmMarkerList[1],
        locationMarkerList = _.zip(locationList, markerList),
        infoWindowList = _.map(locationMarkerList, _.partial(makeInfoWindow, map, infoWindowContent));
    return infoWindowList;
}

///Creates the infoWindows. Requires both the film information and the markers in order to populate the infoWindows,
///so we have to zip those datasets together.
function createInfoWindows(map, filmMarkerLists) {
    var infoWindowsList = _.map(filmMarkerLists, _.partial(makeInfoWindows, map));
    return infoWindowsList;
}
///Updates the markers according to a particular bitmask. If we want to resize the map to the new boundaries (in
///the case that the query is blank or we've chosen a specific film), refocus is set to true.
function makeAssociativeArray(mask, oldMask, markers) {
    var associativeArrayList = [],
        i;
    for (i = 0; i < mask.length; i = i + 1) {
        associativeArrayList.push({
            'mask' : mask[i],
            'oldMask' : oldMask[i],
            'markers' : markers[i],
        });
    }
    return associativeArrayList;
}

function hideMarkerAndWindow(marker) {
    marker.setVisible(false);
    if (FILMLOCATIONS.lastWindow) {
        if (FILMLOCATIONS.lastWindow.marker === marker) {
            FILMLOCATIONS.lastWindow.close();
            FILMLOCATIONS.lastWindow = undefined;
        }
    }
    return marker;
}

function setVisibility(markerUpdate) {
    var visibilitySet;
    if ((markerUpdate.mask === 1) && (markerUpdate.oldMask === 0)) {
        visibilitySet = _.map(markerUpdate.markers, function (marker) { marker.setVisible(true); return marker; });
    } else if ((markerUpdate.mask === 0) && (markerUpdate.oldMask === 1)) {
        visibilitySet = _.map(markerUpdate.markers, hideMarkerAndWindow);
    } else {
        visibilitySet = _.map(markerUpdate.markers, function (marker) { return marker; });
    }
    return visibilitySet;
}

function setMarkerListVisibility(markerUpdates) {
    var visibilityChecked = _.map(markerUpdates, setVisibility);
    return visibilityChecked;
}

function extendUpdateBounds(markerUpdates, bounds) {
    markerUpdates.forEach(function (markerUpdates) {
        if (markerUpdates.mask === 1) {
            bounds = extendBounds(markerUpdates.markers, bounds);
        }
    });
    return bounds;
}

///Gets the new markers to display. Returns a bitmask that tells us which movies' items should be shown. If there's
///no query, we don't have to perform a database lookup (as we want to display all markers), and we want to
///refocus the map. Otherwise, we only refocus when a typeahead text box is clicked.
function updateMarkers(updater, markers, oldMask, map) {
    var mask = updater.mask,
        refocus = updater.refocus,
        markerUpdates = makeAssociativeArray(mask, oldMask, markers),
        bounds = new google.maps.LatLngBounds();
    setMarkerListVisibility(markerUpdates);
    if (refocus === true) {
        bounds = extendUpdateBounds(markerUpdates, bounds);
        resizeMap(bounds, map);
    }
    return {'updater' : updater,
            'markers' : markers,
            'oldMask' : mask};
}

function processQuery(currentOrder, mask, refocus, map) {
    var updater = FILMLOCATIONS.mostRecentUpdate,
        updateAArray;
    FILMLOCATIONS.mostRecentUpdate = {'counter' : currentOrder,
                                      'mask' : mask,
                                      'refocus' : refocus};
    if (FILMLOCATIONS.canUpdateMarkers === true) {
        FILMLOCATIONS.canUpdateMarkers = false;
        while (updater !== FILMLOCATIONS.mostRecentUpdate) {
            updateAArray = updateMarkers(FILMLOCATIONS.mostRecentUpdate, FILMLOCATIONS.markers, FILMLOCATIONS.oldMask, map);
            updater = updateAArray.updater;
            FILMLOCATIONS.markers = updateAArray.markers;
            FILMLOCATIONS.oldMask = updateAArray.oldMask;
        }
        FILMLOCATIONS.canUpdateMarkers = true;
    }
}

function makeQuery(nextQuery, currentOrder, map) {
    if (nextQuery.query === "") {
        processQuery(currentOrder, fillArray(1, FILMLOCATIONS.numberOfMarkers), true, map);
    } else {
        $.get("get_films/?q=" + nextQuery.query, function (mask) {
            if (currentOrder > FILMLOCATIONS.mostRecentUpdate.counter) {
                processQuery(currentOrder, mask, nextQuery.refocus, map);
            }
        });
    }
}

function checkQuery(nextQuery, map) {
    FILMLOCATIONS.nextQuery = nextQuery;
    if ((FILMLOCATIONS.canUpdateData === true) && (nextQuery.query !== FILMLOCATIONS.mostRecentUpdate.query)) {
        FILMLOCATIONS.canUpdateData = false;
        if (FILMLOCATIONS.updateOrder > FILMLOCATIONS.mostRecentUpdate.counter) {
            makeQuery(nextQuery, FILMLOCATIONS.updateOrder, map);
        }
        FILMLOCATIONS.updateOrder = FILMLOCATIONS.updateOrder + 1;
        FILMLOCATIONS.canUpdateData = true;
    }
    if (FILMLOCATIONS.nextQuery !== nextQuery) {
        checkQuery(nextQuery, map);
    }
}

function initializeMap(films, map) {
    var latLngLists = buildLatLngLists(films),
        markerLists = createMarkerLists(map, latLngLists),
        bounds = new google.maps.LatLngBounds();
    bounds = extendMarkerListsBounds(markerLists, bounds);
    resizeMap(bounds, map);
    _.extend(FILMLOCATIONS, initializeFilmLocations(markerLists));
    createInfoWindows(map, _.zip(films, markerLists));
}

