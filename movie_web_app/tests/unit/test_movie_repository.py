from datetime import date, datetime
from typing import List

import pytest

# from movie_web_app.domainmodel.movie import
from movie_web_app.domainmodel.director import Director
from movie_web_app.domainmodel.actor import Actor
# from movie_web_app.domainmodel.genre import
from movie_web_app.domainmodel.model import User,Review, make_review, Movie, Genre
# from movie_web_app.domainmodel.review import
from movie_web_app.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_movie_repo):
    user = User('Dave', '123456789')
    in_movie_repo.add_user(user)

    assert in_movie_repo.get_user('Dave') is user


# def test_repository_can_retrieve_a_user(in_movie_repo):
#     user = in_movie_repo.get_user('fmercury')
#     assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_movie_repo):
    user = in_movie_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_movie_repo):
    number_of_movies = in_movie_repo.get_number_of_movies()

    # Check that the query returned 6 movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_movie_repo):
    movie = Movie("Snow White", 2020)
    in_movie_repo.add_movie(movie)

    assert in_movie_repo.get_movie(1001) is movie

def test_repository_can_add_movies(in_movie_repo):
    movies=[Movie("abc",2020),Movie("def",2021)]
    in_movie_repo.add_movies(movies)

    assert in_movie_repo.get_number_of_movies() == 1002

def test_repository_can_add_actors(in_movie_repo):
    actors = [Actor("abc"), Actor("def"), Actor("jkl")]
    in_movie_repo.add_actors(actors)

    assert len(in_movie_repo.get_actors()) == 1988


def test_repository_can_retrieve_movie(in_movie_repo):
    movie = in_movie_repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_does_not_retrieve_a_non_existent_movie(in_movie_repo):
    movie = in_movie_repo.get_movie(10001)
    assert movie is None


def test_repository_can_search_by_title(in_movie_repo):
    movies = in_movie_repo.get_result("moana")

    # Check that can search by title.
    assert movies[0] == in_movie_repo.get_movie(14)


def test_repository_can_search_by_actor(in_movie_repo):
    movies = in_movie_repo.get_result("Chris Pratt")

    # Check that can search by title.
    assert movies == [Movie("Guardians of the Galaxy", 2014), Movie("Passengers", 2016),
                        Movie("The Magnificent Seven", 2016), Movie("Jurassic World", 2015),
                        Movie("The Lego Movie", 2014), Movie("Zero Dark Thirty", 2012), Movie("10 Years", 2011)]


def test_repository_can_search_by_director(in_movie_repo):
    directors= in_movie_repo.get_result("James Ward Byrkit")

    assert directors == [Movie("Coherence",2013)]


def test_repository_can_search_by_genre(in_movie_repo):
    movies = in_movie_repo.get_result("Action")

    # Check that can search by title.
    assert movies[0] == in_movie_repo.get_movie(1)


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_string(in_movie_repo):
    movies = in_movie_repo.get_result("123")
    assert len(movies) == 0


def test_repository_can_get_first_movie(in_movie_repo):
    movie = in_movie_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_movie_repo):
    movie = in_movie_repo.get_last_movie()
    assert movie.title == 'Nine Lives'


def test_repository_can_get_movies_by_ids(in_movie_repo):
    movies = in_movie_repo.get_movies_by_id([1, 2, 6])

    assert len(movies) == 3
    assert movies[0].title == "Guardians of the Galaxy"
    assert movies[1].title == "Prometheus"
    assert movies[2].title == 'The Great Wall'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_movie_repo):
    movies = in_movie_repo.get_movies_by_id([2, 1000001])

    assert len(movies) == 1
    assert movies[0].title == "Prometheus"


def test_repository_returns_an_empty_list_for_non_existent_ids(in_movie_repo):
    movies = in_movie_repo.get_movies_by_id([0, 2000])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_movie_repo):
    movie_ids = in_movie_repo.get_movie_ids_for_genre('History')

    assert movie_ids == [12,17,44,56,67,71,112,168,169,193,237,253,278,300,334,384,407,472,475,521,523,577,644,673,755,810,868,963,990]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_movie_repo):
    movie_ids = in_movie_repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_year_of_previous_movie(in_movie_repo):
    movie = in_movie_repo.get_movie(6)
    previous_year = in_movie_repo.get_year_of_previous_movie(movie)

    assert previous_year == 2015


def test_repository_returns_none_when_there_are_no_previous_movies(in_movie_repo):
    movie = in_movie_repo.get_movie(831)
    previous_year = in_movie_repo.get_year_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_year_of_next_movie(in_movie_repo):
    movie = in_movie_repo.get_movie(1)
    next_year = in_movie_repo.get_year_of_next_movie(movie)

    assert next_year == 2015


def test_repository_returns_year_of_next_movie_when_no_year_afterwards(in_movie_repo):
    movie = in_movie_repo.get_movie(3)
    next_year = in_movie_repo.get_year_of_next_movie(movie)

    assert next_year == None


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_movie_repo):
    movie = in_movie_repo.get_movie(1000)
    next_title = in_movie_repo.get_year_of_next_movie(movie)

    assert next_title is None


def test_repository_can_add_a_genre(in_movie_repo):
    tag = Genre('Motoring')
    in_movie_repo.add_genre(tag)

    assert tag in in_movie_repo.get_genres()


def test_repository_can_retrieve_movies_by_year(in_movie_repo):
    movies = in_movie_repo.get_movies_by_year(2010)

    # Check that the query returned 3 movies.
    assert len(movies) == 60


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_year(in_movie_repo):
    movies = in_movie_repo.get_movies_by_year(2030)
    assert len(movies) == 0


def test_repository_can_get_first_movie(in_movie_repo):
    movie = in_movie_repo.get_first_movie()
    assert movie == Movie("Guardians of the Galaxy", 2014)


def test_repository_can_get_last_movie(in_movie_repo):
    movie = in_movie_repo.get_last_movie()
    assert movie.title == 'Nine Lives'

    
def test_repository_can_add_a_review(in_movie_repo):
    user = in_movie_repo.get_user('thorke')
    movie = in_movie_repo.get_movie(2)
    review = make_review("Trump's onto it!", user, movie)

    in_movie_repo.add_review(review)

    assert review in in_movie_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_movie_repo):
    movie = in_movie_repo.get_movie(2)
    review = Review(movie, None, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_movie_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_movie_repo):
    user = in_movie_repo.get_user('thorke')
    movie = in_movie_repo.get_movie(2)
    review = Review(None, movie, "Trump's onto it!", datetime.today())

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the movie doesn't refer to the review.
        in_movie_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_movie_repo):
    assert len(in_movie_repo.get_reviews()) == 3

def test_add_favorite_movie(in_movie_repo):
    user = in_movie_repo.get_user('thorke')
    movie = in_movie_repo.get_movie(2)
    in_movie_repo.add_favorite_movie(user,movie)
    assert user.watched_movies == [in_movie_repo.get_movie(2)]

def test_get_watchlist(in_movie_repo):
    user = in_movie_repo.get_user('thorke')
    movie = in_movie_repo.get_movie(2)
    in_movie_repo.add_favorite_movie(user, movie)

    movies= in_movie_repo.get_watchlist(user)
    assert movies == [in_movie_repo.get_movie(2)]



