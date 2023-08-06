from django_filters import rest_framework as filters
from munity.views import MunityGroupableMixin, MunityViewSet
from rest_framework import serializers, viewsets
from django.db.models import Q

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        workspace_id = serializers.SlugField(write_only=True)
        # fields = '__all__'
        fields = [
            "id",
            "workspace",
            "username",
            "email",
            "roles",
            "first_name",
            "last_name",
            "created",
            "is_superuser",
            "modified",
            "generic_groups",
        ]
        model = User
        depth = 1

class UsersFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "workspace": ["exact", "in"],
            "first_name": ["exact", "in", "contains"],
            "generic_groups": ["in"],
            "last_name": ["exact", "in", "contains"],
            "email": ["exact", "in", "contains"],
            "username": ["exact", "in", "contains"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = User


class UsersViewSet(MunityViewSet, MunityGroupableMixin):
    serializer_class = UserSerializer
    filterset_class = UsersFilter

    def perform_create(self, serializer):
        MunityGroupableMixin.perform_create(self, serializer)
        MunityViewSet.perform_create(self, serializer)
    def perform_update(self, serializer):
        MunityGroupableMixin.perform_update(self, serializer)
        MunityViewSet.perform_update(self, serializer)
    def perform_destroy(self, instance):
        MunityGroupableMixin.perform_destroy(self, instance)
        MunityViewSet.perform_destroy(self, instance)


