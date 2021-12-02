Summary:

This is an API developed using Python, Flask and its extension SQLAlchemy.

Files:

app.py - API source code

data.db - SQLite DB with one table 'Movie'. Its fields are -ID, Name, Genre, Language and IMDB rating.

requirements.txt - Packages Needed

Running the API:

1. Go to project root directory in your system terminal
2. Set environment variables: FLASK_APP=APP and FLASK_ENV=development
3. Run the command 'flask run'

The server runs on http://localhost:5000

Endpoints:

/movies - to GET and POST

/movies/<id> - to GET and DELETE one resource

