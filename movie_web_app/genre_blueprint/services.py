from typing import List, Iterable

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import User,Review,Movie ,make_review,Genre
# from movie_web_app.domainmodel.genre import
import movie_web_app.adapters.repository as repo


class NonExistentmovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids

def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentmovieException

    return movie_to_dict(movie)

# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'year': movie.year,
        'title': movie.title,
        'description': movie.description,
        # 'hyperlink': movie.hyperlink,
        # 'image_hyperlink': movie.image_hyperlink,
        'reviews': reviews_to_dict(movie.reviews),
        'genres': genres_to_dict(movie.genres)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]

def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.user_name,
        'movie_id': review.rating,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genreged_movies': [movie.id for movie in repo.repo_instance.get_result(genre.genre_name)]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.year)
    movie.id=dict.id
    movie.description = dict.description
    movie.hyperlink = dict.hyperlink
    # Note there's no reviews or genres.
    return movie

