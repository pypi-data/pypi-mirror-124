from functools import wraps
from typing import Callable, Any
from roughrider.predicate.errors import ConstraintError


PredicateErrorHandler = Callable[[ConstraintError], Any]


def with_predicates(predicates, handler=None):
    def predication_wrapper(func):
        @wraps(func)
        def assert_predicates(*args, **kwargs):
            for predicate in predicates:
                try:
                    predicate(*args, **kwargs)
                except ConstraintError as exc:
                    if handler is not None:
                        return handler(exc)
                    raise
            return func(*args, **kwargs)
        return assert_predicates
    return predication_wrapper
