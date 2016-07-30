## Justbake Scraper

### Installation
* pip install -r requirements.txt
* change database settings (database, user, password host, port) in settings.py line# 81
* python manage.py migrate
* python manage.py runserver
* Got to 127.0.0.0.1:8000 in browser
* Click on Fetch cakes, This will atleast 15 minutes depending on your internet speed.
* Export Excel and Json from respective button on menu bar

### Search and Filters
##### Base URL: /api/cakes/

* ?search = < search string >
* ?max_price = < price >
* ?min_price = < price >
* ?category_id = < category pk >
