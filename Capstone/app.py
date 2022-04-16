import os
import datetime
from flask import Flask, jsonify, request, abort
from models import setup_db, Actor, Movie
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    return app

app = create_app()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

'''
Movie API end points
'''

@app.route('/movies')
@requires_auth('get:movies')
def get_movies(jwt):
    movies = Movie.query.all()

    if not movies:
        abort(404)
    
    movies_list = [movie.format() for movie in movies]

    return jsonify({
        'success': True,
        'movies': movies_list,
        'total': len(movies_list)
    })

@app.route('/movies/<id>')
@requires_auth('get:movies')
def get_movie(jwt,id):
    movie = Movie.query.filter(Movie.id==id).one_or_none()

    if not movie:
        abort(404)
    
    movie_details = movie.format()

    return jsonify({
        'success': True,
        'movie': movie_details

    })

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movie(jwt):
    data = request.get_json()
    title = data.get('title')
    category = data.get('category')
    release_date = data.get('release_date')
    release_date_fmt = datetime.datetime.strptime(release_date,"%Y-%m-%d")

    if not title:
        abort(422)

    try:

        movie = Movie(title=title, category=category, release_date=release_date_fmt)
        movie.insert()

        return jsonify({
        'success': True,
        'movie': movie.format()

    })
    except:
        abort(422)




@app.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt,id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
        abort(404)
    movie.delete()

    return jsonify({
        'success': True,
        'movie': id
    })

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(jwt,id):
    data = request.get_json()
    new_title = data.get('title')
    new_category = data.get('category')
    new_release_date = data.get('release_date')
    new_release_date_fmt = datetime.datetime.strptime(new_release_date,"%Y-%m-%d")

    movie = Movie.query.filter(Movie.id==id).one_or_none()

    if not movie:
        abort(404)
    
    movie.title = new_title
    movie.category = new_category
    movie.release_date = new_release_date_fmt

    try:
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    except:
        abort(422)

'''
Actor API endpoints
'''


@app.route('/actors')
@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()

    if not actors:
        abort(404)
    
    actors_list = [actor.format() for actor in actors]

    return jsonify({
        'success': True,
        'actors': actors_list,
        'total': len(actors_list)
    })

@app.route('/actors/<id>')
@requires_auth('get:actors')
def get_actor(jwt,id):
    actor = Actor.query.filter(Actor.id==id).one_or_none()

    if not Actor:
        abort(404)
    
    Actor_details = Actor.format()

    return jsonify({
        'success': True,
        'Actor': Actor_details

    })

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actor(jwt):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    if not name:
        abort(422)

    try:

        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
        'success': True,
        'actor': actor.format()

    })
    except:
        abort(422)




@app.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt,id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
        abort(404)
    try:
        actor.delete()

        return jsonify({
            'success': True,
            'actor': id
        })
    except: 
        abort(422)


@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actor(jwt,id):
    data = request.get_json()
    new_name = data.get('name')
    new_age = data.get('age')
    new_gender = data.get('gender')

    actor = Actor.query.filter(Actor.id==id).one_or_none()

    if not actor:
        abort(404)
    
    if not (new_name):
        abort(422)
    
    actor.name = new_name
    actor.age = new_age
    actor.gender = new_gender

    try:
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except:
        abort(422)




'''
Error handling functions
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.__dict__
    }), error.status_code





if __name__ == '__main__':
    app.run()
