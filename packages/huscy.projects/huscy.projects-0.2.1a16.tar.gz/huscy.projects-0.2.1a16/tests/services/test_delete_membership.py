import pytest

from huscy.projects.models import Membership
from huscy.projects.services import create_membership, delete_membership

pytestmark = pytest.mark.django_db


def test_remove_membership(project, user):
    membership = create_membership(project, user, is_coordinator=True)

    assert user.has_perm('view_project', project)
    assert user.has_perm('change_project', project)

    delete_membership(membership)

    assert not user.has_perm('view_project', project)
    assert not user.has_perm('change_project', project)
    assert not Membership.objects.exists()
