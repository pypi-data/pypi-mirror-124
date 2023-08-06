import pytest
from roughrider.predicate.errors import (
    ConstraintError, HTTPConstraintError, ConstraintsErrors,
)


def test_httperror_malformed():
    with pytest.raises(TypeError) as exc:
        HTTPConstraintError()

    assert str(exc.value) == (
        "__init__() missing 2 required positional arguments: "
        "'message' and 'status'"
    )

    with pytest.raises(TypeError) as exc:
        HTTPConstraintError(message='test')

    assert str(exc.value) == (
        "__init__() missing 1 required positional argument: 'status'")

    with pytest.raises(TypeError) as exc:
        HTTPConstraintError(status=200)

    assert str(exc.value) == (
        "__init__() missing 1 required positional argument: 'message'")

    with pytest.raises(ValueError) as exc:
        HTTPConstraintError(message='test', status='abc')

    assert str(exc.value) == "'abc' is not a valid HTTPStatus"


def test_httperror():
    error = HTTPConstraintError(message='test', status=400)
    assert error == HTTPConstraintError(message='test', status=400)

    with pytest.raises(AttributeError) as exc:
        error.message = 'I am immutable'

    with pytest.raises(AttributeError) as exc:
        error.status = 200

    error = HTTPConstraintError('test', 400)
    assert error == HTTPConstraintError(message='test', status=400)


def test_httperrors():
    error1 = ConstraintError('test 1')
    error2 = HTTPConstraintError('test 2', 400)

    errors = ConstraintsErrors(error1, error2)
    assert len(errors) == 2
    assert errors == ConstraintsErrors(error1, error2)
    assert errors == [error1, error2]
    assert not errors == (error1, error2)

    assert errors.json() == (
        '''[{"message": "test 1"}, {"message": "test 2"}]'''
    )
