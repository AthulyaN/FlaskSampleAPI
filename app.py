# A Flask server app implementing an API that interfaces to an SQLite DB
# Basic HTTP error codes have been implemented
# TODO - Exception handling

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# Defining the model for Table Movie
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    language = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f"{self.name} - {self.language} - {self.genre} - {self.rating}"


@app.route('/')
def hello():
    return 'Hello!'


# For GET request to http://localhost:5000/movies
@app.route('/movies')
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_data = {'Id': movie.id, 'Name': movie.name, 'Language': movie.language,
                      'Genre': movie.genre, 'IMDB rating': movie.rating}
        movie_list.append(movie_data)
    return {"Movies": movie_list}, 200


# For GET request to http://localhost:5000/movies/<id>
@app.route('/movies/<id>')
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify({'Id': movie.id, 'Name': movie.name, 'Language': movie.language,
                    'Genre': movie.genre, 'IMDB rating': movie.rating})


# For POST request to http://localhost:5000/movies
@app.route('/movies', methods=['POST'])
def add_movie():
    if request.is_json:
        movie = Movie(name=request.json['Name'], language=request.json['Language'],
                      genre=request.json['Genre'], rating=request.json['IMDB rating'])
        db.session.add(movie)
        db.session.commit()
        return jsonify({'Id': movie.id, 'Name': movie.name, 'Language': movie.language,
                        'Genre': movie.genre, 'IMDB rating': movie.rating}), 201
    else:
        return {'error': 'Request must be JSON'}, 400


# For PUT request to http://localhost:5000/movies/<id>
@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    if request.is_json:
        movie = Movie.query.get(id)
        if movie is None:
            return {'error': 'not found'}, 404
        else:
            movie.name = request.json['Name']
            movie.language = request.json['Language']
            movie.genre = request.json['Genre']
            movie.rating = request.json['IMDB rating']
            db.session.commit()
            return 'Updated', 200
    else:
        return {'error': 'Request must be JSON'}, 400


# For DELETE request to http://localhost:5000/movies/<id>
@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
        return {'error': 'not found'}, 404
    db.session.delete(movie)
    db.session.commit()
    return f'{id} is deleted', 200
