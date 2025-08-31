from rest_framework import viewsets, filters, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as django_filters
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsOwner, IsAdminOrSelf
from django.utils import timezone


# Registration endpoint
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# User CRUD
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()


# Filters for tasks
class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    priority = django_filters.CharFilter(field_name="priority", lookup_expr="iexact")
    due_date_before = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")
    due_date_after = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Task
        fields = ["status", "priority", "due_date"]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ["due_date", "priority"]
    ordering = ["due_date"]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Completed':
            return Response({"error": "Task is already completed."}, status=status.HTTP_400_BAD_REQUEST)
        task.mark_complete()
        return Response({"message": "Task marked as completed."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Pending':
            return Response({"error": "Task is already pending."}, status=status.HTTP_400_BAD_REQUEST)
        task.mark_incomplete()
        return Response({"message": "Task reverted to pending."}, status=status.HTTP_200_OK)