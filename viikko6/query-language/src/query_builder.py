from matchers import All, PlaysIn, HasAtLeast, HasFewerThan, And, Or, Not


class QueryBuilder:
    def __init__(self, matcher=All()):
        self._matcher = matcher

    def plays_in(self, team):
        return QueryBuilder(And(self._matcher, PlaysIn(team)))

    def has_at_least(self, value, attr):
        return QueryBuilder(And(self._matcher, HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(And(self._matcher, HasFewerThan(value, attr)))

    def one_of(self, *builders):
        matchers = [builder._matcher for builder in builders]
        return QueryBuilder(Or(*matchers))

    def not_(self, matcher):
        return QueryBuilder(Not(matcher))

    def build(self):
        return self._matcher
