import pytest
from model_bakery import baker

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_403_FORBIDDEN)

pytestmark = pytest.mark.django_db


@pytest.fixture
def principal_investigator(django_user_model):
    return baker.make(django_user_model)


def test_admin_user_can_create_research_units(admin_client, principal_investigator):
    response = create_research_unit(admin_client, principal_investigator)

    assert response.status_code == HTTP_201_CREATED


def test_admin_user_can_delete_research_units(admin_client, research_unit):
    response = delete_research_unit(admin_client, research_unit)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_admin_user_can_list_research_units(admin_client):
    response = list_research_units(admin_client)

    assert response.status_code == HTTP_200_OK


def test_admin_user_can_partial_update_research_units(admin_client, research_unit):
    response = partial_update_research_unit(admin_client, research_unit)

    assert response.status_code == HTTP_200_OK


def test_admin_user_can_update_research_units(admin_client, research_unit, principal_investigator):
    response = update_research_unit(admin_client, research_unit, principal_investigator)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_create_research_units(client, user, principal_investigator):
    create_permission = Permission.objects.get(codename='add_researchunit')
    user.user_permissions.add(create_permission)

    response = create_research_unit(client, principal_investigator)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_can_delete_research_units(client, user, research_unit):
    create_permission = Permission.objects.get(codename='delete_researchunit')
    user.user_permissions.add(create_permission)

    response = delete_research_unit(client, research_unit)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_partial_update_research_units(client, user, research_unit):
    update_permission = Permission.objects.get(codename='change_researchunit')
    user.user_permissions.add(update_permission)

    response = partial_update_research_unit(client, research_unit)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_update_research_units(client, user, research_unit,
                                                        principal_investigator):
    update_permission = Permission.objects.get(codename='change_researchunit')
    user.user_permissions.add(update_permission)

    response = update_research_unit(client, research_unit, principal_investigator)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_create_research_units(client, principal_investigator):
    response = create_research_unit(client, principal_investigator)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_without_permission_cannot_delete_research_units(client, research_unit):
    response = delete_research_unit(client, research_unit)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_without_permission_can_list_research_units(client):
    response = list_research_units(client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_partial_update_research_units(client, research_unit):
    response = partial_update_research_unit(client, research_unit)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_without_permission_cannot_update_research_units(client, research_unit,
                                                              principal_investigator):
    response = update_research_unit(client, research_unit, principal_investigator)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_research_units(anonymous_client, principal_investigator):
    response = create_research_unit(anonymous_client, principal_investigator)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_delete_research_units(anonymous_client, research_unit):
    response = delete_research_unit(anonymous_client, research_unit)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_list_research_units(anonymous_client):
    response = list_research_units(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_partial_update_research_units(anonymous_client, research_unit):
    response = partial_update_research_unit(anonymous_client, research_unit)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_update_research_units(anonymous_client, research_unit,
                                                     principal_investigator):
    response = update_research_unit(anonymous_client, research_unit, principal_investigator)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_research_unit(client, user):
    return client.post(
        reverse('researchunit-list'),
        data=dict(name='research_unit', code='RU', principal_investigator=user.pk)
    )


def delete_research_unit(client, research_unit):
    return client.delete(reverse('researchunit-detail', kwargs=dict(pk=research_unit.id)))


def list_research_units(client):
    return client.get(reverse('researchunit-list'))


def partial_update_research_unit(client, research_unit):
    return client.patch(
        reverse('researchunit-detail', kwargs=dict(pk=research_unit.id)),
        data=dict(name='research_unit_2', code='RU2')
    )


def update_research_unit(client, research_unit, principal_investigator):
    return client.put(
        reverse('researchunit-detail', kwargs=dict(pk=research_unit.id)),
        data=dict(
            name='research_unit_2',
            code='RU2',
            principal_investigator=principal_investigator.pk
        )
    )
