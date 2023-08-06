import pytest

from django.db import IntegrityError

from huscy.projects.models import Membership
from huscy.projects.services import create_membership

pytestmark = pytest.mark.django_db


def test_add_normal_member(project, user):
    assert not Membership.objects.exists()

    create_membership(project, user)

    membership = Membership.objects.get(project=project, user=user)
    assert membership.is_coordinator is False
    assert user.has_perm('view_project', project)
    assert not user.has_perm('change_project', project)


def test_add_member_as_coordinator(project, user):
    assert not Membership.objects.exists()

    create_membership(project, user, is_coordinator=True)

    membership = Membership.objects.get(project=project, user=user)
    assert membership.is_coordinator is True
    assert user.has_perm('view_project', project)
    assert user.has_perm('change_project', project)


def test_add_member_with_write_permission(project, user):
    assert not Membership.objects.exists()

    create_membership(project, user, has_write_permission=True)

    membership = Membership.objects.get(project=project, user=user)
    assert membership.is_coordinator is False
    assert user.has_perm('view_project', project)
    assert user.has_perm('change_project', project)


def test_has_write_permission_is_ignored_if_is_coordinator_is_set_to_true(project, user):
    assert not Membership.objects.exists()

    create_membership(project, user, is_coordinator=True, has_write_permission=False)

    membership = Membership.objects.get(project=project, user=user)
    assert membership.is_coordinator is True
    assert user.has_perm('view_project', project)
    assert user.has_perm('change_project', project)


def test_add_member_twice_to_project_fails(project, user):
    assert not Membership.objects.exists()

    create_membership(project, user)
    with pytest.raises(IntegrityError):
        create_membership(project, user)
