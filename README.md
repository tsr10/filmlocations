This is my implementation of the San Francisco Film Data coding challenge.

This project is deployed to Heroku, and you can access it at: https://secure-everglades-6319.herokuapp.com/

This solution focuses on the full-stack.


Description of the problem and solution
---------------
In the San Francisco film data assignment, the challenge is to plot all of the movie shoot information in the San Francisco Film Database onto a Google map that supports a typeahead autocomplete bar and that filters the displayed markers according to this search bar.

Usage of the app should be self-explanatory.


To run locally
---------------
You will need to have npm, git, and mongodb/mongod installed. Preferably, this should be done within a virtualenv. In a separate tab, run:
`mongod`

While that's running, run:
`pip install -r requirements.txt`
`./manage.py syncdb`
`./manage.py loaddata backupdb.json`
`./manage.py runserver`

(You can ignore the mongodb-engine error that occurs during the pip install.)

You should now have the service running on your computer. Go to `localhost:8000` in Chrome to see it.

As a note, I've included the bower packages as part of this distribution. If this were a formal release, I'd be operating within a Virtual Machine and would configure it to install bower and the dependencies. For the purposes of the project, though, I'll omit it. I'm also running the script using a backupdb.json file - I can only call the Geolocation API a set number of times per day and I didn't want to run the risk of going over the limit given that three engineers will be reviewing this code. If this were going to real production, I'd also look at configuring the API keys via environment variables, etc.


My implementation details
---------------
This database only contained addresses and not lat/lng co-ordinates, so I code the data using Google's Geolocation API using the management command find_lat_lng.

This isn't a very large dataset, so it should be loaded onto the website for quicker access and searching. I ended up storing the data using MongoDB, as the strict hierarchy of film -> location and the need for quick access made a document store a good choice.

The second was how to plot all of the data points. I ended up dumping the database to a new .json file, allShoots.json, that includes all films' titles with location information for each shoot that occurred.

When the website loads, we want to see all of the points - so on browser load, we just go through this file and create every marker and infoWindow.

I implemented a typeahead search bar using the typeahead.js library. The autocomplete section of the search bar is fairly standard, though there is probably a library that can better sort the typeahead results for relevance - if I had more time, I would have looked into it.

The main question of this assignment, then, was how to filter these datapoints using the typeahead search bar. Attempting to do this client-side would be costly - this is an operation that would be better done server-side. So when we make a query, we send it to the server. The server then returns a list where each element is either 0 or 1 (in the code, I call this a mask, due to its similarity to a bitmask) - it generates this list by seeing which films match the supplied query. Note that we order allFilms.json and this query by film title, so the ordering of this list is the same as the ordering of allFilms.json. So if the server returns a list where the tenth element is 1, then we should show all of the markers that are related to the 10th movie in allFilms.json. I also keep track of what the last mask we processed was, and only update those markers whose state has changed. This requires fewer operations than iterating through the entire mask every time.

For efficiency's sake, if a blank query is entered, we don't bother sending it to the server - we know that all markers should be displayed, so we simply return a mask of all ones.

Because queries run asynchronously, we need to be careful in what order queries were entered. We only want to update the map if we get a query that was made after the last one we ran. So we keep track of this state using the FILMLOCATIONS.mostRecentQuery associative array, and by keeping a counter that dictates in what order the queries were made. Thus, when updating the map, we can check to make sure our query is more recent than the one in mostRecentUpdate using the FILMLOCATIONS.mostRecentQuery.counter variable and comparing it to the FILMLOCATIONS.updateOrder variable.

Overall, I'm very happy with how my solution came out. There could definitely stand to be more tests, including Selenium-based browser tests, but I figured that was overly robust for the scale of this project.


Code
----------------
The main code that I've written and expect to be evaluated on is in:
autocomplete/views.py
locationstore/management/commands/find_lat_long.py
locationstore/management/commands/load_film_data.py
locationstore/models.py
map/views.py
templates/index.html
static/css/style.scss
static/js/marker-updates.js
testing/qunit/tests.html
testing/tests.py

The rest is mostly Django boilerplate, perhaps with a few trivial things added (such as in locationstore/admin.py, locationstore/views.py, and filmlocations/urls.py). The file static/js/mapstyle.js is from an open-source website.


Dependencies
---------------
The bower_components module stores the .js libraries that the site uses. These libraries are JQuery, Bootstrap, Typeahead, and Handlebars. JQuery is used with Javascript to perform all of the functions necessary for the single page app. Bootstrap is used to style the webpage. Typeahead is used to make the typeahead bar work. Handlebars is used to help style the typeahead bar and the infowindow. Underscore is used to maintain a more functional style in handling the Javascript (for ease of testing).


Back-end
---------------
I implemented this in Django because it's a framework I'm familiar with and it makes it easy to configure a lot of the details and dependencies for the project. I have a lot of familiarity with it, and I really like writing backend code in Python. There are only three different URLs that the app refers to in usage - the root URL, autocomplete, and get_films. The root URL is how the app is accessed, the autocomplete view is called by Typeahead, and get_shoots is used to populate the map.


Front-end
---------------
After speccing out the requirements, I decided that Javascript and JQuery would be sufficient to implement this app. If it were more complicated, I'd have looked into Backbone. The only .html page is index.html, and the only other javascript I've written is in static/js/marker-updates.js.

Database structure
---------------
The site uses a MongoDB backend. There's only one table in the database that stores each movie's info. We only filter
by film, so there isn't a good reason to use any additional tables.
