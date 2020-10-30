from datetime import date, datetime

import pytest

from movie_web_app.adapters.database_repository import SqlAlchemyRepository
from movie_web_app.domainmodel.model import User, Movie, Genre, Review, make_review
from movie_web_app.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user.username.title() == User('fmercury', '8734gfe2058v').username.title()

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    # Check that the query returned 177 movies.
    assert number_of_movies == 1000

def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    new_movie_id = number_of_movies + 1

    movie = Movie(
        "Tenet",2020
    )
    movie.id=new_movie_id
    movie.description="A great movie"
    repo.add_movie(movie)

    assert repo.get_movie(new_movie_id) == movie

def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the movie is reviewed as expected.
    review_one = [review for review in movie.reviews if review.review_text == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    review_two = [review for review in movie.reviews if review.review_text == 'Yeah Freddie, bad news'][0]

    assert review_one.user.username == 'fmercury'
    assert review_two.user.username == "thorke"

    # Check that the movie is genreged as expected.

    assert movie.is_genred_by(Genre('Action'))
    assert movie.is_genred_by(Genre('Adventure'))

def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(2010)
    assert movie is None

def test_repository_can_retrieve_movies_by_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_year(2006)

    # Check that the query returned 3 movies.
    assert len(movies) == 44

    # these movies are no jokes...
    movies = repo.get_movies_by_year(2016)

    # Check that the query returned 5 movies.
    assert len(movies) == 297

def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_year(2020)
    assert len(movies) == 0

def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 20
    # print(genres)
    genre_one = [genre for genre in genres if genre.genre_name == 'Action'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'History'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Thriller'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Horror'][0]

    assert genre_one.number_of_genred_movies == 303
    assert genre_two.number_of_genred_movies == 29
    assert genre_three.number_of_genred_movies == 195
    assert genre_four.number_of_genred_movies == 119

def test_repository_can_get_first_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'

def test_repository_can_get_last_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_last_movie()
    assert movie.title == 'Nine Lives'

def test_repository_can_get_movies_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 5, 6])

    assert len(movies) == 3
    assert movies[
               0].title == 'Prometheus'
    assert movies[1].title == "Suicide Squad"
    assert movies[2].title == 'The Great Wall'

def test_repository_does_not_retrieve_movie_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 209])

    assert len(movies) == 2
    assert movies[
               0].title == 'Prometheus'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([0, 199])

    assert len(movies) == 1

def test_repository_returns_movie_ids_for_existing_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('History')

    assert movie_ids == [12,17,44,56,67,71,112,168,169,193,237,253,278,
 300,
 334,
 384,
 407,
 472,
 475,
 521,
 523,
 577,
 644,
 673,
 755,
 810,
 868,
 963,
 990]

def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('Morning')

    assert len(movie_ids) == 0


def test_repository_returns_year_of_previous_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(6)
    previous_year = repo.get_year_of_previous_movie(movie)

    assert previous_year == 2015


def test_repository_returns_none_when_there_are_no_previous_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(446)
    previous_year = repo.get_year_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_year_of_next_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(2)
    next_year = repo.get_year_of_next_movie(movie)

    assert next_year == 2013


def test_repository_returns_none_when_there_are_no_subsequent_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(7)
    next_year = repo.get_year_of_next_movie(movie)

    assert next_year is None


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Motoring')
    repo.add_genre(genre)

    assert genre in repo.get_genres()


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    movie = repo.get_movie(2)
    review = make_review("Trump's onto it!", user, movie)

    repo.add_review(review)

    assert review in repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(2)
    review = Review(movie,None, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 3


def make_movie(new_movie_year):
    movie = Movie(
        new_movie_year,
        'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
        'The self-isolation deadline has been pushed back',
        'https://www.nzherald.co.nz/business/news/movie.cfm?c_id=3&objectid=12316800',
        'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
    )
    return movie

def test_can_retrieve_an_movie_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch movie and User.
    movie = repo.get_movie(5)
    author = repo.get_user('thorke')

    # Create a new review, connecting it to the movie and User.
    review = make_review('First death in Australia', author, movie)

    movie_fetched = repo.get_movie(5)
    author_fetched = repo.get_user('thorke')

    assert review in movie_fetched.reviews
    assert review in author_fetched.reviews

