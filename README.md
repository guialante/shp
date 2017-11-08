## About this project

Project to store address and location points clicked on a map
in a sqlite database and google fusion tables as well

## `locations` django app
In this app is defined the models to store the address points, the view to show the map and stored addresses, the views to 
handle the map click events via ajax to save each point or to reset data stored.

## Scripts
Use jQuery, and the gmaps JS library, also in the `static/js/project.js` is the logic in charge to execute the 
AJAX request and init the map.

# How to execute it

```
    $ git clone https://github.com/guialante/shp.git          
    $ virtualenv .ve
    $ .ve\scripts\activate
    $ pip install -r requirements/base.txt
    $ ./manage.py migrate
    $ ./manage.py runserver
```

## Running Tests
```
    $ .ve\scripts\activate
    $ py.test
```