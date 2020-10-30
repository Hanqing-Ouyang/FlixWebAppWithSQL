from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        from ..movie_blueprint import movie
        app.register_blueprint(movie.movie_blueprint)