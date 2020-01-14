import uuid

import pytest


@pytest.fixture
def test_pw():
    return "a-strong-one"


@pytest.fixture
def create_user(db, django_user_model, test_pw):
    def make_user(**kwargs):
        if "password" not in kwargs:
            kwargs["password"] = test_pw
        if "username" not in kwargs:
            kwargs["username"] = uuid.uuid4()
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def mk_logged_in_client(db, client, create_user, test_pw):
    def make_logged_in_client(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_pw)
        return user, client

    return make_logged_in_client
