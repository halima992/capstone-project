import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor,Movie
from auth.auth import AuthError, requires_auth
ENV = 'deploy'
def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # This endpoint for check if app is running
    @app.route('/')
    def get_greeting():
        greeting = "Hello,This app work for back-end not for front-end" 
        return greeting
    

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(jwt):
      ''' handling GET requests for all available actors'''
      # get  all available actors
      actors = Actor.query.order_by(Actor.id).all()
      # paginating actors
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 20
      end = start + 20
      # formatted actors
      formatted_actors = [actor.format() for actor in actors]
      current_actors = formatted_actors[start:end]
      # abort if there is no retrived actors
      if len(current_actors) == 0:
            abort(404)
      # return actors as json by this endpoint
      return jsonify({'success': True, 'actors':current_actors})

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(jwt):
      ''' handling GET requests for all available movies'''
      # get  all available movies
      movies = Movie.query.order_by(Movie.id).all()
      # paginating movies
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + 10
      # formatted movies
      formatted_movies = [movie.format() for movie in movies]
      current_movies   = formatted_movies[start:end]
      # abort if there is no retrived movies
      if len(current_movies) == 0:
            abort(404)
      # return movies as json by this endpoint
      return jsonify({'success': True, 'movies':current_movies})
    
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actors(jwt):
      '''handling POST requests to add a new actors'''
      # load data of request body as json and assign it to variables
      body = request.get_json()
      actor = body.get('actor', None)
      gender = body.get('gender', None)
      movie = body.get('movie',None)
      # find any actor holding the same name of new actor
      actors = Actor.query.order_by(Actor.id).filter(Actor.actor==actor).all()
      # abort if there is actor holding the same name
      if len(actors)!=0:
        abort(400)
      # if actor is unique post it
      else:
        try:
          new_actor = Actor(actor=actor,gender=gender,movie=movie)
          new_actor.insert()
          return jsonify({'success': True})
        # the exception could be happen if there is null coulmn may gender , movie or  actor
        except:
          abort(422)
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movies(jwt):
      '''handling POST requests to add a new movie'''
      # load data of request body as json and assign it to variables
      body = request.get_json()
      movie = body.get('movie',None)
      catogry = body.get('catogry',None)
      # find any movie holding the same name of new movie
      movies = Movie.query.order_by(Movie.id).filter(Movie.movie==movie).all()
      # abort if there is movie holding the same name
      if len(movies)!=0:
        abort(400)
      # if movie is unique post it
      else:
        try:
          new_movie = Movie(movie=movie,catogry=catogry)
          new_movie.insert()
          return jsonify({'success': True})
        # the exception could be happen if there is null coulmn may  movie or  catogary
        except:
          abort(422)
    
    @app.route('/actors/<int:actor_id>',methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt,actor_id):
      '''handling DELETE requests for deleting actor using an id of the actor '''
      # get the selected actor by id
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      # abort if there is no selected actor -> actor by this id not found
      if actor is None:
        abort(404)
      # delete actor if is found
      else:
        actor.delete()
        return jsonify({'success': True, 'Deleted': actor_id})
        
    @app.route('/movies/<int:movie_id>',methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt,movie_id):
      '''handling DELETE requests for deleting movie using an id of the movie '''
      # get the selected movie by id
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      # abort if there is no selected movie -> movie by this id not found
      if movie is None:
        abort(404)
      # delete movie if is found
      else:
        movie.delete()
        return jsonify({'success': True, 'Deleted': movie_id})

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt,actor_id):
      '''handling PATCH requests for updating actor using an id of the actor '''
      # get the selected actor by id
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      # abort if there is no selected actor -> actor by this id not found
      if actor is None:
        abort(404)
      # update actor if is found
      else:
        try:
          # load data of request body as json and assign it to variables
          body = request.get_json()
          if "actor" in body:
              actor.actor = body.get('actor')
          if "gender" in body:
              actor.gender = body.get('gender')
          if "movie" in body:
              actor.movie = body.get('movie')
          #made modification
          actor.update()
          return jsonify({"success": True, "actor": [actor.format()]})
        except BaseException:
          abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt,movie_id):
      '''handling PATCH requests for updating movie using an id of the movie '''
      # get the selected movie by id
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      # abort if there is no selected movie -> movie by this id not found
      if movie is None:
        abort(404)
      # update movie if is found
      else:
        try:
          # load data of request body as json and assign it to variables
          body = request.get_json()
          if "movie" in body:
              movie.movie = body.get('movie')
          if "catogry" in body:
              movie.catogry = body.get('catogry')
          #made modification
          movie.update()
          return jsonify({"success": True, "movie": [movie.format()]})
        except BaseException:
          abort(422)


    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400 
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    '''implement error handler for AuthError'''
    @app.errorhandler(AuthError)
    def error_handler(exception):
        respond = jsonify(exception.error)
        respond.status_code = exception.status_code
        return respond
    return app
app = create_app()

if __name__ == '__main__':
  if ENV == 'develop':
        app.run(host='0.0.0.0', port=8080, debug=True)
  else:
        app.run(debug=False)
    