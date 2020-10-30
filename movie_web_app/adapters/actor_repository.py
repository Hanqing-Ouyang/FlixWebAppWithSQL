import abc
from typing import List

from movie_web_app.domainmodel.actor import Actor

repo_actors = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name: str):
        raise NotImplementedError


class ActorRepository(AbstractRepository):

    def __init__(self, args:list):
        self._actor: List[Actor] = list()
        #self._actor=args

        for actor in args:
            self._actor.append(actor)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._actor):
            raise StopIteration
        else:
            self._current += 1
            return self._actor[self._current-1]

    def get_actor(self, actor_full_name: str):
        return next((actor for actor in self._actor if actor.actor_full_name== actor_full_name), None)
