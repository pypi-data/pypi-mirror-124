from itertools import cycle

import pytest
from model_bakery import baker

from huscy.projects.services import get_memberships

pytestmark = pytest.mark.django_db


@pytest.fixture
def projects():
    return baker.make('projects.Project', _quantity=3)


@pytest.fixture
def users(django_user_model):
    return baker.make(django_user_model, _quantity=3)


@pytest.fixture
def memberships(projects, users):
    return baker.make('projects.Membership', project=cycle(projects), user=cycle(users),
                      _quantity=3)


def test_get_memberships(projects, users, memberships):
    project = projects[0]

    result = get_memberships(project)

    assert len(result) == 1
    assert result[0].project == project
    assert result[0].user == users[0]
