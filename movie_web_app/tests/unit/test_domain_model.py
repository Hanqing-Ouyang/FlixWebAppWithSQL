from datetime import date

from movie_web_app.domainmodel.director import Director
from movie_web_app.domainmodel.actor import Actor
# from movie_web_app.domainmodel.genre import
from movie_web_app.domainmodel.model import User,Review,Movie,make_review,Genre
import pytest


@pytest.fixture()
def movie():
    return Movie("Molly", 2018 )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('New Zealand')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for review in user.reviews:
        # User should have an empty list of reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.year == 2018
    assert movie.title == 'Molly'

    assert movie.reviews == []
    assert len(movie.genres) == 0

    assert repr(
        movie) == '<Movie Molly, 2018>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        None, 2010
    )

    movie_2 = Movie(
        None, 2012
    )

    assert movie_1 < movie_2



def test_make_review_establishes_relationships(movie, user):
    review_text = 'COVID-19 in the USA!'
    review = make_review(review_text, user, movie)

    # Check that the User object knows about the review.
    assert review in user.reviews

    # Check that the review knows about the User.
    assert review.user is user

    # Check that movie knows about the review.
    assert review in movie.reviews

    # Check that the review knows about the movie.
    assert review.movie is movie

def test_watchlist(user,movie):
    user.watch_movie(movie)
    assert user.watched_movies == [Movie("Molly",2018)]