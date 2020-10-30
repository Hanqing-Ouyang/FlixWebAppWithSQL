import abc
from typing import List

from movie_web_app.domainmodel.director import Director

repo_directors = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name: str):
        raise NotImplementedError


class DirectorRepository(AbstractRepository):

    def __init__(self, args:list):
        self._director: List[Director] = list()
        #self._director=args

        for director in args:
            self._director.append(director)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._director):
            raise StopIteration
        else:
            self._current += 1
            return self._director[self._current-1]

    def get_director(self, director_full_name: str):
        return next((director for director in self._director if director.director_full_name==director_full_name), None)
