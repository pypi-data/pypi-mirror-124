import logging

from django.db.models import Q
from django.db.transaction import atomic
from guardian.shortcuts import assign_perm, remove_perm

from huscy.projects.models import Membership, Project, ResearchUnit

logger = logging.getLogger('projects')


@atomic
def create_membership(project, user, is_coordinator=False, has_write_permission=False):
    assign_perm('view_project', user, project)
    if is_coordinator or has_write_permission:
        assign_perm('change_project', user, project)
    return Membership.objects.create(
        project=project,
        user=user,
        is_coordinator=is_coordinator,
    )


@atomic
def create_project(title, research_unit, principal_investigator, creator,
                   local_id=None, description=''):
    if local_id is None:
        local_id = Project.objects.get_next_local_id(research_unit)

    project = Project.objects.create(
        description=description,
        local_id=local_id,
        principal_investigator=principal_investigator,
        research_unit=research_unit,
        title=title,
    )
    logger.info('Project id:%d, local_id_name:%s, title:%s reserch_unit:%s has been created',
                project.id, project.local_id_name, project.title, project.research_unit.name)

    create_membership(project, principal_investigator, is_coordinator=True)
    if principal_investigator != creator:
        create_membership(project, creator, is_coordinator=True)

    return project


@atomic
def delete_membership(membership):
    remove_perm('view_project', membership.user, membership.project)
    remove_perm('change_project', membership.user, membership.project)
    membership.delete()


@atomic
def delete_project(project):
    map(delete_membership, project.membership_set.all())
    logger.info('All members from project <id: %d> removed', project.id)

    project.delete()
    logger.info('Project id:%d, local_id_name:%s, title:%s research_unit:%s has been deleted',
                project.id, project.local_id_name, project.title, project.research_unit.name)


def get_memberships(project):
    return Membership.objects.filter(project=project).order_by('project__id', 'user__id')


def get_participating_projects(user):
    return (Project.objects
                   .filter(Q(principal_investigator=user) | Q(membership__user=user))
                   .distinct())


def get_projects():
    return Project.objects.all()


def get_research_units():
    return ResearchUnit.objects.order_by('name')


def update_membership(membership, is_coordinator, has_write_permission):
    if is_coordinator or has_write_permission:
        assign_perm('change_project', membership.user, membership.project)
    else:
        remove_perm('change_project', membership.user, membership.project)
    membership.is_coordinator = is_coordinator
    membership.save()
    return membership
