# from movie_web_app.domainmodel.movie import Movie
# from movie_web_app.domainmodel.review import Review
from datetime import datetime
# from movie_web_app.domainmodel.genre import Genre
from movie_web_app.domainmodel.actor import Actor
from movie_web_app.domainmodel.director import Director
from typing import List, Iterable


class User:

    def __init__(
            self, username: str, password: str
    ):
        if username == "" or type(username) is not str:
            self._username = None
        else:
            self._username = username.strip().title()
        self._password: str = password
        self._watched_movies = []
        self._reviews = []
        self._time_spent_watching_movies_minutes = 0

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username):
        if username == "" or type(username) is not str:
            self._username = None
        else:
            self._username = username.strip().title()

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password):
        if type(password) is str:
            self._password = password.strip()

    @property
    def watched_movies(self) -> list:
        return self._watched_movies

    @watched_movies.setter
    def watched_movies(self, watched_movies):
        self._watched_movies = watched_movies

    @property
    def reviews(self) -> Iterable['Review']:
        return self._reviews

    @reviews.setter
    def reviews(self, reviews:'Review'):
        self._reviews = reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self._time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, time_spent_watching_movies_minutes):
        if type(time_spent_watching_movies_minutes) is int:
            if int(time_spent_watching_movies_minutes) > 0:
                self._time_spent_watching_movies_minutes = time_spent_watching_movies_minutes

    def __repr__(self):
        return f'<User {self._username.title()}>'

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
                other._username == self._username
        )

    def __lt__(self, other):
        if isinstance(other, User):
            return ((self._username) < (other._username))

    def __hash__(self):
        ty = str(self._username)
        return hash(ty)

    def watch_movie(self, movie: 'Movie'):
        self._watched_movies.append(movie)
        # self._time_spent_watching_movies_minutes = self._time_spent_watching_movies_minutes + movie.runtime_minutes

    def add_review(self, review: 'Review'):
        if isinstance(review, Review):
            self._reviews.append(review)

    def remove_review(self, review: str, movie: 'Movie'):
        for i in self._reviews:
            if (i._review_text == review) and (i._movie == movie):
                self._reviews.remove(i)


class Movie:

    def __init__(
            self, title: str, year: int
    ):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()
        if type(year) is not int:
            self._year = None
        elif year < 1900:
            self._year = None
        else:
            self._year = year
        self._id: int = None
        self._description: str = None
        self._director: Director = None
        self._actors = []
        self._genres = []
        self._reviews = []
        self._runtime_minutes: int = None

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title:str):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id):
        if id == "" or type(id) is not int:
            self._id = None
        else:
            self._id = id

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, year):
        if type(year) is not int:
            self._year = None
        elif year < 1900:
            self._year = None
        else:
            self._year = year

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description):
        if type(description) is str:
            self._description = description.strip()

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, director):
        if isinstance(director, Director):
            self._director = director

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if type(runtime_minutes) is int:
            if int(runtime_minutes) > 0:
                self._runtime_minutes = runtime_minutes
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def actors(self) -> list:
        return self._actors

    @actors.setter
    def actors(self, actors):
        self._actors = actors

    @property
    def genres(self) -> list:
        return self._genres

    @genres.setter
    def genres(self, genres):
        self._genres = genres

    @property
    def reviews(self) -> Iterable['Review']:
        return self._reviews

    @reviews.setter
    def reviews(self, reviews:Iterable['Review']):
        self._reviews = reviews

    def is_genred_by(self, genre: 'Genre'):
        return (genre in self._genres)

    def is_genred(self) -> bool:
        return len(self._genres) > 0

    def number_of_genres(self) -> int:
        return len(self._genres)


    def number_of_reviews(self) -> int:
        return len(self._reviews)

    def add_actor(self, actor: Actor):
        if isinstance(actor, Actor):
            self._actors.append(actor)

    def remove_actor(self, actor: Actor):
        if isinstance(actor, Actor):
            if actor in self._actors:
                self._actors.remove(actor)

    def add_genre(self, genre: 'Genre'):
        if isinstance(genre, Genre):
            self._genres.append(genre)

    def remove_genre(self, genre: 'Genre'):
        if isinstance(genre, Genre):
            if genre in self._genres:
                self._genres.remove(genre)

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def remove_review(self, review: 'Review'):
        if isinstance(review, Review):
            if review in self._reviews:
                self._reviews.remove(review)


    def __repr__(self):
        return f'<Movie {self._title}, {self._year}>'

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return (
                other._title == self._title and
                other._year == self._year
        )

    def __lt__(self, other):
        if isinstance(other, Movie):
            return self._year < other._year

    def __hash__(self):
        ty = str(self._title) + str(self._year)
        return hash(ty)


class Review:

    def __init__(
            self, movie: 'Movie', user: User, review_text: str, timestamp: datetime
    ):
        if not isinstance(movie, Movie):
            self._movie = Movie("None", None)
        else:
            self._movie = movie
        if type(review_text) is str:
            self._review_text = review_text.strip()
        else:
            self._review_text = None

        self._user = user

        self._rating = None
        if isinstance(timestamp, datetime):
            self._timestamp = timestamp
        else:
            self._timestamp = datetime.now()

    @property
    def movie(self) -> "Movie":
        return self._movie

    @movie.setter
    def movie(self, movie):
        if isinstance(movie, Movie):
            self._movie = movie

    @property
    def user(self) -> "User":
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, rating):
        if rating <= 10 and rating >= 1:
            self._rating = rating
        else:
            self._rating = None

    @property
    def review_text(self) -> str:
        return self._review_text

    @review_text.setter
    def review_text(self, review_text):
        if type(review_text) is str:
            self._review_text = review_text.strip()

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if isinstance(timestamp, datetime):
            self._timestamp = timestamp

    def __repr__(self):
        return f'<Review {self._movie}, {self._review_text}, {self._rating}, {self._timestamp}>'

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return (
                other._movie == self._movie and
                other._review_text == self._review_text and
                other._rating == self._rating and
                other._timestamp == self._timestamp
        )


class Genre:
    def __init__(
            self, genre_name: str,
    ):
        self._genre_name: str = genre_name
        self._genred_movies: List[Movie] = list()

    @property
    def genre_name(self) -> str:
        return self._genre_name

    @property
    def genred_movies(self) -> list:
        return self._genred_movies

    # @property
    # def genreged_movies(self, ) -> str:
    #     return self._genre_name

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self._genred_movies

    def add_movie(self, movie: Movie):
        self._genred_movies.append(movie)
        
    @property
    def number_of_genred_movies(self) -> int:
        return len(self._genred_movies)

    def __repr__(self):
        if not self._genre_name:
            return f'<Genre None>'
        else:
            return f'<Genre {self._genre_name}>'

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return (
                other._genre_name == self._genre_name
        )

    def __lt__(self, other):
        return self._genre_name < other._genre_name

    def __hash__(self):
        return hash(self._genre_name)




class ModelException(Exception):
    pass


def make_review(review_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    review = Review(movie, user, review_text, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review

def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'genre {genre.genre_name} already applied to movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)

