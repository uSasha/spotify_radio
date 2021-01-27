import pytest


# TODO: not used in tests due to parametrize
@pytest.fixture
def users():
    return ['wotetsaz6dvmgp02mv8fcwfvo', 'no_such_user']


@pytest.fixture
def stations():
    return ['21jrjoe0YmFdSildIeZEyz', '1qH4QR427LghS8CFKy4sbd']
