from typing import List, Iterable

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import User,Review,Movie ,make_review,Genre
# from movie_web_app.domainmodel.genre import
import movie_web_app.adapters.repository as repo


class NonExistentmovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(int(movie_id))
    if movie is None:
        raise NonExistentmovieException

    user = repo.get_user(username)
    # print("movie_user", user)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, movie)
    # print("movie_user2", review)
    # Upyear the repository.
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentmovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_year(year, repo: AbstractRepository):
    # Returns movies for the target year (empty if no matches), the year of the previous movie (might be null), the year of the next movie (might be null)

    movies = repo.get_movies_by_year(year)

    movies_dto = list()
    prev_year = next_year = None

    if len(movies) > 0:
        prev_year = repo.get_year_of_previous_movie(movies[0])
        next_year = repo.get_year_of_next_movie(movies[0])

        # Convert movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentmovieException

    return reviews_to_dict(movie.reviews)

def get_watchlist_for_user(username, repo: AbstractRepository) ->list:
    user=repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return repo.get_watchlist(user)

def get_movie_ids(movie_list):
    ids=[]
    for a in movie_list:
        ids.append(int(a.id))
    return ids


def add_movie_to_watchlist(username, movie_id, repo: AbstractRepository):
    user = repo.get_user(username)
    movie = repo.get_movie(movie_id)
    if user is None:
        raise UnknownUserException
    repo.add_favorite_movie(user,movie)

# def get_watchlist(repo: AbstractRepository):
#     return repo.get_watchlist(user)


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
        'username': review.user.username,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'genre_name': genre.genre_name,
        'genred_movies': [movie.id for movie in genre.genred_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]

def user_to_dict(user: User):
    user_dict = {
        'name': user.username,
        '_watched_movies': user.watched_movies,
        'reviews': user.reviews
    }
    return user_dict

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
