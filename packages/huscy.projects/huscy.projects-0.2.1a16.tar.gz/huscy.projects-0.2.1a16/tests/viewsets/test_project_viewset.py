import pytest
from model_bakery import baker

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
                                   HTTP_405_METHOD_NOT_ALLOWED)

from huscy.projects.models import Project

pytestmark = pytest.mark.django_db


def test_retrieve_not_allowed(client, project):
    response = retrieve_project(client, project)

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_admin_user_can_create_projects(admin_client, admin_user, research_unit):
    response = create_project(admin_client, research_unit, admin_user)

    assert response.status_code == HTTP_201_CREATED


def test_admin_user_can_delete_projects(admin_client, project):
    response = delete_project(admin_client, project)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_admin_user_can_list_projects(admin_client):
    response = list_projects(admin_client)

    assert response.status_code == HTTP_200_OK


def test_admin_user_can_partial_update_projects(admin_client, project):
    response = partial_update_project(admin_client, project)

    assert response.status_code == HTTP_200_OK


def test_admin_user_can_update_projects(admin_client, project):
    response = update_project(admin_client, project)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_delete_projects(client, user, project):
    delete_permission = Permission.objects.get(codename='delete_project')
    user.user_permissions.add(delete_permission)

    response = delete_project(client, project)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_partial_update_research_units(client, user, project):
    update_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(update_permission)

    response = partial_update_project(client, project)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_update_projects(client, user, project):
    update_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(update_permission)

    response = update_project(client, project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_create_projects(client, user, research_unit):
    response = create_project(client, research_unit, user)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_cannot_delete_projects(client, project):
    response = delete_project(client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_without_permission_can_list_projects(client):
    response = list_projects(client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_partial_update_projects(client, project):
    response = partial_update_project(client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_without_permission_cannot_update_projects(client, project):
    response = update_project(client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_projects(anonymous_client, user, research_unit):
    response = create_project(anonymous_client, research_unit, user)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_delete_projects(anonymous_client, project):
    response = delete_project(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_list_projects(anonymous_client):
    response = list_projects(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_partial_update_projects(anonymous_client, project):
    response = partial_update_project(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_update_projects(anonymous_client, project):
    response = update_project(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_create_project_with_existing_local_id(client, user, research_unit):
    baker.make('projects.Project', research_unit=research_unit, local_id=166)
    response = create_project(client, research_unit, user, local_id=166)

    assert response.status_code == HTTP_400_BAD_REQUEST
    error_msg = response.json()['non_field_errors']
    assert error_msg == ['The fields local_id, research_unit must make a unique set.']


def test_user_cannot_update_local_id_to_other_existing_local_id(client, user, project):
    update_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(update_permission)

    other = baker.make('projects.Project', research_unit=project.research_unit,
                       local_id=project.local_id + 1)

    response = update_project(client, project, local_id=other.local_id)

    assert response.status_code == HTTP_400_BAD_REQUEST


def test_user_can_update_local_id_to_unused_local_id(client, user, project):
    update_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(update_permission)

    assert not Project.objects.filter(local_id=project.local_id + 1,
                                      research_unit=project.research_unit).exists()
    response = update_project(client, project, local_id=project.local_id + 1)

    assert response.status_code == HTTP_200_OK

    assert not Project.objects.filter(local_id=project.local_id,
                                      research_unit=project.research_unit).exists()


def create_project(client, research_unit, principal_investigator=None, local_id=None):
    data = dict(
        description='project_description',
        principal_investigator=principal_investigator.pk,
        research_unit=research_unit.id,
        title='project_title',
    )
    if local_id:
        data['local_id'] = local_id

    return client.post(reverse('project-list'), data=data)


def delete_project(client, project):
    return client.delete(reverse('project-detail', kwargs=dict(pk=project.pk)))


def list_projects(client):
    return client.get(reverse('project-list'))


def partial_update_project(client, project):
    return client.patch(
        reverse('project-detail', kwargs=dict(pk=project.pk)),
        data=dict(title='new_project_title')
    )


def retrieve_project(client, project):
    return client.get(reverse('project-detail', kwargs=dict(pk=project.pk)))


def update_project(client, project, local_id=None):
    return client.put(
        reverse('project-detail', kwargs=dict(pk=project.pk)),
        data=dict(
            description=project.description,
            principal_investigator=project.principal_investigator.id,
            research_unit=project.research_unit.pk,
            title='new_project_title',
            local_id=local_id or project.local_id,
        )
    )
