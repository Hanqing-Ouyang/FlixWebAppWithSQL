
class Actor:
    pass

    def __init__(
            self, actor_full_name: str,
    ):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self._actor_full_name=None
        else:
            self._actor_full_name=actor_full_name.strip()

        self._colleagues = []


    @property
    def actor_full_name(self):
        return self._actor_full_name

    @actor_full_name.setter
    def actor_full_name(self,value):
        if value == "" or type(value) is not str:
            self._actor_full_name = None
        else:
            self._actor_full_name=value.strip()

    def __repr__(self) -> str:
        return f'<Actor {self._actor_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return (
                other._actor_full_name == self._actor_full_name
        )

    def __lt__(self, other:'Actor'):
        if not isinstance(other, Actor):
            return False
        else:
            return self._actor_full_name < other._actor_full_name

    def __hash__(self):
        return hash(self._actor_full_name)

    def add_actor_colleague(self, colleague:'Actor'):
        if isinstance(colleague, Actor):
            self._colleagues.append(colleague)
            colleague._colleagues.append(self)
        else:
            return False

    def check_if_this_actor_worked_with(self, colleague:'Actor') -> bool:
        if not isinstance(colleague, Actor):
            return False
        else:
            return colleague in self._colleagues

class TestActorMethods:

    def test_init(self):
        actor1 = Actor("Angelina Jolie")
        print(actor1)
        assert repr(actor1) == "<Actor Angelina Jolie>"
        actor2 = Actor("")
        print(actor2)
        assert actor2.actor_full_name is None
        actor3 = Actor(42)
        print(actor3)
        assert actor3.actor_full_name is None

        actor3 = Actor("Brad Pitt")
        print(actor3)
        assert repr(actor3) == "<Actor Brad Pitt>"
        actor5 = Actor("Cameron123")
        print(actor5)
        assert repr(actor5) == "<Actor Cameron123>"

        actor3.add_actor_colleague(actor1)
        print(actor3.check_if_this_actor_worked_with(actor1))
        assert (actor3.check_if_this_actor_worked_with(actor1)) == True
        print(actor2.check_if_this_actor_worked_with(actor1))
        assert not (actor2.check_if_this_actor_worked_with(actor1))

        actor3.add_actor_colleague("AA")
        actor3.add_actor_colleague("<Actor None>")
        actor3.add_actor_colleague("<Actor Max>")
        assert repr(actor3._colleagues) == "[<Actor Angelina Jolie>]"
        actor3.add_actor_colleague(Actor("Max"))
        print(actor3._colleagues)
        assert repr(actor3._colleagues) == "[<Actor Angelina Jolie>, <Actor Max>]"
        print(actor1._colleagues)
        assert repr(actor1._colleagues) == "[<Actor Brad Pitt>]"
        print("aaaaaa")
        print(actor3.check_if_this_actor_worked_with("AA"))
        assert not (actor3.check_if_this_actor_worked_with("AA"))
        print(actor3.check_if_this_actor_worked_with(Actor("AA")))
        assert not (actor3.check_if_this_actor_worked_with(Actor("AA")))

        print(actor1.__lt__(actor3))
        assert (actor1.__lt__(actor3))
        print(actor1.__lt__("AA"))
        assert not (actor1.__lt__("AA"))

