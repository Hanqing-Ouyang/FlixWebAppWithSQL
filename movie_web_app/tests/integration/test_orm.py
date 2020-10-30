import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from movie_web_app.domainmodel.model import User, Movie, Review, Genre, make_review,make_genre_association

# movie_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_movie(empty_session):
    empty_session.execute(
        "INSERT INTO movies ( id, title, description, year) VALUES "
        "(1001, 'Tenet', "
        "'it is a good movie',"
        "2020)"
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("News"), ("New Zealand")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie_genre_associations(empty_session, movie_key, genre_keys):
    stmt = 'INSERT INTO movie_genres (movie_id, genre_id) VALUES (:movie_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'movie_id': movie_key, 'genre_id': genre_key})


def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)
    #
    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, movie_id, review_text, timestamp) VALUES '
        '(:user_id, :movie_id, "review 1", :timestamp_1),'
        '(:user_id, :movie_id, "review 2", :timestamp_2)',
        {'user_id': user_key, 'movie_id': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def make_movie():
    movie = Movie(
        "Tenet", 2020
    )
    movie.id=1001
    movie.description='it is a good movie'
    return movie


def make_user():
    user = User("Andrew", "111")
    return user


def make_genre():
    genre = Genre("News")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]

    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie
    assert movie_key == fetched_movie.id


def test_loading_of_genreged_movie(empty_session):
    movie_key = insert_movie(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_movie_genre_associations(empty_session, movie_key, genre_keys)

    movie = empty_session.query(Movie).get(movie_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert movie.is_genred_by(genre)
        assert genre.is_applied_to(movie)


def test_loading_of_reviewed_movie(empty_session):
    insert_reviewed_movie(empty_session)

    rows = empty_session.query(Movie).all()
    movie = rows[0]

    assert len(movie._reviews) == 2

    for review in movie._reviews:
        assert review._movie is movie


def test_saving_of_review(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Movie).all()
    movie = rows[0]
    user = empty_session.query(User).filter(User._username == "Andrew").one()

    # Create a new review that is bidirectionally linked with the User and movie.
    review_text = "Some review text."
    review = make_review(review_text, user, movie)

    # Note: if the bidirectional links between the new review and the User and
    # movie objects hadn't been established in memory, they would exist following
    # committing the addition of the review to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))

    assert rows == [(user_key, movie_key, review_text)]


def test_saving_of_movie(empty_session):
    movie = make_movie()
    empty_session.add(movie)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title, description, year FROM movies'))

    assert rows == [(1001, 'Tenet', 'it is a good movie', 2020)]


def test_saving_genreged_movie(empty_session):
    movie = make_movie()
    genre = make_genre()

    # Establish the bidirectional relationship between the movie and the genre.
    make_genre_association(movie, genre)

    # Persist the movie (and genre).
    # Note: it doesn't matter whether we add the genre or the movie. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_movie() checks for insertion into the movies table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT id, genre_name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][1] == "News"

    # Check that the movie_genres table has a new record.
    rows = list(empty_session.execute('SELECT movie_id, genre_id from movie_genres'))
    movie_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert movie_key == movie_foreign_key
    assert genre_key == genre_foreign_key


def test_save_reviewed_movie(empty_session):
    # Create movie User objects.
    movie = make_movie()
    user = make_user()

    # Create a new review that is bidirectionally linked with the User and movie.
    review_text = "Some review text."
    review = make_review(review_text, user, movie)

    # Save the new movie.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_movie() checks for insertion into the movies table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that links to the movies and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))
    assert rows == [(user_key, movie_key, review_text)]