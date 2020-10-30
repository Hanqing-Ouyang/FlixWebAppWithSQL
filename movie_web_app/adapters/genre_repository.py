import abc
from typing import List

from movie_web_app.domainmodel.model import Genre

repo_genres = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name: str):
        raise NotImplementedError

class GenreRepository(AbstractRepository):

    def __init__(self, args:list):
        self._genre: List[Genre] = list()
        #self._genre=args

        for genre in args:
            self._genre.append(genre)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._genre):
            raise StopIteration
        else:
            self._current += 1
            return self._genre[self._current-1]

    def get_genre(self, genre_name: str):
        return next((genre for genre in self._genre if genre.genre_name == genre_name), None)