from rest_framework import viewsets
from munity.generic_groups.models import GenericGroup
from django.db.models.query_utils import Q

from munity.workspaces.models import Workspace

# Create your views here.
class MunityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.serializer_class.Meta.model

        if "workspace_pk" in self.kwargs:
            return model.objects.filter(Q(workspace=self.kwargs["workspace_pk"]))
        return model.objects.all()

    def perform_destroy(self, instance):
        pass

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.request.data
        if "workspace" in data:
            instance.workspace_id = data["workspace"]
            instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        data = self.request.data
        if "workspace" in data:
            instance.workspace_id = data["workspace"]
            instance.save()

class MunityGroupableMixin(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.request.data
        if "generic_groups" in data:
            groups = GenericGroup.objects.filter(pk__in=data["generic_groups"])
            instance.generic_groups.set(groups)

    def perform_update(self, serializer):
        instance = serializer.save()
        data = self.request.data
        if "generic_groups" in data:
            groups = GenericGroup.objects.filter(pk__in=data["generic_groups"])
            instance.generic_groups.set(groups)

    def perform_destroy(self, instance):
        instance.generic_groups.set([])
        instance.delete()