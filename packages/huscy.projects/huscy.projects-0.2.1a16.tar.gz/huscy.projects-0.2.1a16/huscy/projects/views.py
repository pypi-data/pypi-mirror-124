import logging

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser

from huscy.projects import serializer, services
from huscy.projects.helpers import get_client_ip
from huscy.projects.models import Project
from huscy.projects.permissions import AllowAnyToCreate, IsProjectCoordinator, ReadOnly

logger = logging.getLogger('projects')


class MembershipViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.MembershipSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsProjectCoordinator | ReadOnly)

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return services.get_memberships(self.project)

    def perform_create(self, serializer):
        serializer.save(project=self.project)

    def perform_destroy(self, membership):
        services.delete_membership(membership)


class ProjectViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.ProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions | AllowAnyToCreate)

    def get_queryset(self):
        return services.get_projects()

    def perform_create(self, serializer):
        logger.info('User %s from IP %s requested creation of new project',
                    self.request.user.username, get_client_ip(self.request))
        serializer.save()

    def perform_destroy(self, project):
        logger.info('User %s from IP %s requested deletion of project with id:%d',
                    self.request.user.username, get_client_ip(self.request), project.id)
        services.delete_project(project)


class ResearchUnitViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_research_units()
    serializer_class = serializer.ResearchUnitSerializer
