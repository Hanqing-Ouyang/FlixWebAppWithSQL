from movie_web_app.domainmodel.model import Genre
from movie_web_app.domainmodel.actor import Actor
from movie_web_app.domainmodel.director import Director
# from movie_web_app.domainmodel.user import Review

class Movie:
    pass

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
        self._id: int=None
        self._description: str=None
        self._director: Director=None
        self._actors = []
        self._genres = []
        self._reviews = []
        self._runtime_minutes: int= None


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title):
        if title == "" or type(title) is not str:
            self._title= None
        else:
            self._title=title.strip()

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
        elif year <1900:
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
    def runtime_minutes(self) ->int:
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self,runtime_minutes):
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
    def reviews(self) -> list:
        return self._reviews

    @reviews.setter
    def reviews(self, reviews):
        self._reviews = reviews

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
        ty=str(self._title)+str(self._year)
        return hash(ty)

    def add_actor(self,actor:Actor):
        if isinstance(actor, Actor):
            self._actors.append(actor)

    def remove_actor(self,actor:Actor):
        if isinstance(actor, Actor):
            if actor in self._actors:
                self._actors.remove(actor)

    def add_genre(self,genre:Genre):
        if isinstance(genre, Genre):
            self._genres.append(genre)

    def remove_genre(self,genre:Genre):
        if isinstance(genre, Genre):
            if genre in self._genres:
                self._genres.remove(genre)

    # def add_review(self,review:Review):
    #     if isinstance(review, Review):
    #         self._reviews.append(review)
    #
    # def remove_review(self,review:Review):
    #     if isinstance(review, Review):
    #         if review in self._reviews:
    #             self._reviews.remove(review)


class TestMovieMethods:

    def test_init(self):

        movie = Movie("Moana", 2016)
        print(movie)
        assert repr(movie) == "<Movie Moana, 2016>"
        director = Director("Ron Clements")
        movie.director = director
        print(movie.director)
        assert repr(movie.director) == "<Director Ron Clements>"

        actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
        for actor in actors:
            movie.add_actor(actor)
        print(movie.actors)
        assert repr(movie.actors)== "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"

        movie.runtime_minutes = 107
        print("Movie runtime: {} minutes".format(movie.runtime_minutes))
        assert movie.runtime_minutes == 107

        movie2 = Movie("Moana", 2016)
        print(movie2)
        assert repr(movie) == "<Movie Moana, 2016>"

        movie3 = Movie("Moana", 1996)
        print(movie3)
        assert repr(movie3) == "<Movie Moana, 1996>"

        movie4 = Movie("", 1996)
        print(movie4)
        assert repr(movie4) == "<Movie None, 1996>"

        movie5 = Movie("24", 1)
        print(movie5)
        assert repr(movie5) == "<Movie None, None>"

        movie6 = Movie("", 1)
        print(movie6)
        assert repr(movie6) == "<Movie None, 1996>"

        print(movie.__eq__(movie2))
        assert True
        print(movie.__hash__() == movie2.__hash__())
        assert True
        print(movie.__hash__())
        print(movie3.__hash__())
        print(movie.__hash__() == movie3.__hash__())
        assert not (movie.__hash__() == movie3.__hash__())

        movie.add_genre(Genre("Horror"))
        print(movie.genres)
        assert repr(movie.genres) == "[<Genre Horror>]"
        movie.remove_genre(Genre("aa"))
        print(movie.genres)
        assert repr(movie.genres) == "[<Genre Horror>]"
        movie.remove_genre(Genre("Horror"))
        print(movie.genres)
        assert repr(movie.genres) == "[]"

        movie.add_actor(Actor("Jaro"))
        print(movie.actors)
        assert repr(
            movie.actors) == "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>, <Actor Jaro>]"

        movie.remove_actor(Actor("Auli'i Cravalho"))
        print(movie.actors)
        assert repr(
            movie.actors) == "[<Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>, <Actor Jaro>]"
