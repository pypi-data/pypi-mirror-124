import json
from http import HTTPStatus
from dataclasses import dataclass, InitVar, asdict
from typing import List, Iterable, TypeVar


HTTPCode = TypeVar('HTTPCode', HTTPStatus, int)


@dataclass(frozen=True)
class ConstraintError(Exception):
    message: str


@dataclass(frozen=True)
class HTTPConstraintError(ConstraintError):
    status: InitVar[HTTPCode]

    def __post_init__(self, status):
        super().__setattr__('status', HTTPStatus(status))


class ConstraintsErrors(Exception):
    errors: List[ConstraintError]

    def __init__(self, *errors: ConstraintError):
        self.errors = list(errors)

    def __iter__(self):
        return iter(self.errors)

    def __len__(self):
        return len(self.errors)

    def __eq__(self, other):
        if isinstance(other, ConstraintsErrors):
            return self.errors == other.errors
        elif isinstance(other, Iterable):
            return self.errors == other
        return False

    def json(self):
        return json.dumps([asdict(e) for e in self.errors])
