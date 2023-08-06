from django_filters import rest_framework as filters
from munity.views import MunityGroupableMixin, MunityViewSet
from rest_framework import serializers

from .models import GenericGroup


class GenericGroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "label",
            "generic_groups",
            "created",
            "modified",
        ]
        depth = 1
        model = GenericGroup


class GenericGroupsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "label": ["exact", "in", "contains"],
            "generic_groups": ["in"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = GenericGroup


class GenericGroupsViewSet(MunityViewSet, MunityGroupableMixin):
    serializer_class = GenericGroupSerializer
    filterset_class = GenericGroupsFilter

    def perform_create(self, serializer):
        MunityGroupableMixin.perform_create(self, serializer)
        MunityViewSet.perform_create(self, serializer)
    def perform_update(self, serializer):
        MunityGroupableMixin.perform_update(self, serializer)
        MunityViewSet.perform_update(self, serializer)
    def perform_destroy(self, instance):
        MunityGroupableMixin.perform_destroy(self, instance)
        MunityViewSet.perform_destroy(self, instance)

