from model_bakery import baker

from huscy.projects.services import create_membership, get_participating_projects


def test_no_project_participation(admin_user):
    users_project = get_participating_projects(admin_user).values_list('id', flat=True)
    assert list(users_project) == []


def test_pi_participated_projects(user, admin_user):
    pi_project = baker.make('projects.Project', principal_investigator=user)
    user_projects = get_participating_projects(user).values_list('id', flat=True)
    assert list(user_projects) == [pi_project.id]


def test_member_projects(user, project):
    user_projects = get_participating_projects(user).values_list('id', flat=True)
    assert list(user_projects) == []

    create_membership(project, user)

    user_projects = get_participating_projects(user).values_list('id', flat=True)
    assert list(user_projects) == [project.id]


def test_pi_and_member_projects(user):
    pi_project = baker.make('projects.Project', principal_investigator=user)
    member_project = baker.make('projects.Project')

    create_membership(member_project, user)

    user_projects = get_participating_projects(user).values_list('id', flat=True)
    assert sorted(user_projects) == sorted([pi_project.id, member_project.id])


def test_pi_and_member_are_the_same(user):
    pi_project = baker.make('projects.Project', principal_investigator=user)
    create_membership(pi_project, user)

    user_projects = get_participating_projects(user).values_list('id', flat=True)
    assert list(user_projects) == [pi_project.id]
