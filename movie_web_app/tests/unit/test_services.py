from datetime import datetime

import pytest

from movie_web_app.authentication.services import AuthenticationException
from movie_web_app.movie_blueprint import services as news_services
from movie_web_app.authentication import services as auth_services
from movie_web_app.movie_blueprint.services import NonExistentmovieException


def test_can_add_user(in_movie_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_movie_repo)

    user_as_dict = auth_services.get_user(new_username, in_movie_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_movie_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_movie_repo)


def test_authentication_with_valid_credentials(in_movie_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_movie_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_movie_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_movie_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_movie_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_movie_repo)


def test_can_add_review(in_movie_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the review.
    news_services.add_review(movie_id, review_text, username, in_movie_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = news_services.get_reviews_for_movie(movie_id, in_movie_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_movie_repo):
    movie_id = 1001
    review_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(news_services.NonExistentmovieException):
        news_services.add_review(movie_id, review_text, username, in_movie_repo)


def test_cannot_add_review_by_unknown_user(in_movie_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(news_services.UnknownUserException):
        news_services.add_review(movie_id, review_text, username, in_movie_repo)


def test_can_get_movie(in_movie_repo):
    movie_id = 2

    movie_as_dict = news_services.get_movie(movie_id, in_movie_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == 2012
    assert movie_as_dict['title'] == 'Prometheus'
    #assert movie_as_dict['first_para'] == 'US President Trump tweeted on Saturday night (US time) that he has asked the Centres for Disease Control and Prevention to issue a ""strong Travel Advisory"" but that a quarantine on the New York region"" will not be necessary.'
    assert len(movie_as_dict['reviews']) == 0

    genre_names = [dictionary['name'] for dictionary in movie_as_dict['genres']]
    assert len(genre_names) == 3


def test_cannot_get_movie_with_non_existent_id(in_movie_repo):
    movie_id = 7000

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(news_services.NonExistentmovieException):
        news_services.get_movie(movie_id, in_movie_repo)


def test_get_first_movie(in_movie_repo):
    movie_as_dict = news_services.get_first_movie(in_movie_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_movie_repo):
    movie_as_dict = news_services.get_last_movie(in_movie_repo)

    assert movie_as_dict['id'] == 1000


def test_get_movies_by_year_with_one_year(in_movie_repo):
    target_year = 2007

    movies_as_dict, prev_year, next_year = news_services.get_movies_by_year(target_year, in_movie_repo)

    assert len(movies_as_dict) == 53
    assert movies_as_dict[0]['id'] == 40

    assert prev_year == 2006
    assert next_year == 2008


def test_get_movies_by_year_with_multiple_years(in_movie_repo):
    target_year = 2010

    movies_as_dict, prev_year, next_year = news_services.get_movies_by_year(target_year, in_movie_repo)

    # Check that there are 3 movies yeard 2020-03-01.
    assert len(movies_as_dict) == 60

    # Check that the movie ids for the the movies returned are 3, 4 and 5.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([81, 139, 220]).issubset(movie_ids)

    # Check that the years of movies surrounding the target_year are 2020-02-29 and 2020-03-05.
    assert prev_year == 2009
    assert next_year == 2011


def test_get_movies_by_year_with_non_existent_year(in_movie_repo):
    target_year = 2020

    movies_as_dict, prev_year, next_year = news_services.get_movies_by_year(target_year, in_movie_repo)

    # Check that there are no movies yeard 2020-03-06.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_movie_repo):
    target_movie_ids = [5, 6, 7, 8]
    movies_as_dict = news_services.get_movies_by_id(target_movie_ids, in_movie_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 4

    # Check that the movie ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([5, 6]).issubset(movie_ids)


def test_get_reviews_for_movie(in_movie_repo):
    reviews_as_dict = news_services.get_reviews_for_movie(1, in_movie_repo)

    # Check that 2 reviews were returned for movie with id 1.
    assert len(reviews_as_dict) == 3

    # # Check that the reviews relate to the movie whose id is 1.
    # movie_ids = [review['movie_id'] for review in reviews_as_dict]
    # movie_ids = set(movie_ids)
    # assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_movie_repo):
    with pytest.raises(NonExistentmovieException):
        reviews_as_dict = news_services.get_reviews_for_movie(1001, in_movie_repo)


def test_get_reviews_for_movie_without_reviews(in_movie_repo):
    reviews_as_dict = news_services.get_reviews_for_movie(2, in_movie_repo)
    assert len(reviews_as_dict) == 0

def test_add_movie_to_watchlist(in_movie_repo):
    username = 'thorke'
    movie_id=2
    user = in_movie_repo.get_user(username)
    news_services.add_movie_to_watchlist(username,movie_id,in_movie_repo)
    assert user.watched_movies== [in_movie_repo.get_movie(2)]

def test_get_watchlist(in_movie_repo):
    username = 'thorke'
    movie_id = 2
    user = in_movie_repo.get_user(username)
    news_services.add_movie_to_watchlist(username, movie_id, in_movie_repo)

    movies= news_services.get_watchlist_for_user('thorke',in_movie_repo)
    assert movies == [in_movie_repo.get_movie(2)]

