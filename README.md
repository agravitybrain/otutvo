# otutvo

We parse information from web-sites about online intership programs.<br>
Then we store information in mongodb database.<br>
The user can interract with our app via a web-site, where he/she can easily access stored data, using the given filters.<br>


- **parser.py** - parses full info about internships offerings using Beautiful Soup 4 and requests.<br>
- **db_work.py** - connects to the Mongo DB database using pymongo module. Searches for courses in the database that satisfy given filters. Uses geopy to get latitude and longitude of the given cities of the internship companies. <br>
- **map_generator.py** generates map using folium module. <br>
- **app.py** flask app that runs our web-site.

