from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data.get("email", ""))
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "status",
            "completed_at",
            "created_at",
            "updated_at",
            "owner",
        ]
        read_only_fields = ["id", "status", "completed_at", "created_at", "updated_at"]

    def validate_due_date(self, value):
        # due_date is a date field; ensure it's in the future (not today or past)
        if value and value <= timezone.localdate():
            raise serializers.ValidationError("Due date must be a future date.")
        return value

    def validate(self, attrs):
        """
        Prevent editing fields of a task that is already completed.
        Only allow reverting status from 'Completed' -> 'Pending' (to enable edits).
        """
        instance = getattr(self, "instance", None)
        if instance and instance.status == "Completed":
            # If trying to revert to Pending, allow that
            if attrs.get("status") == "Pending":
                return attrs
            # If any other changes beyond status, block
            non_status_changes = {k: v for k, v in attrs.items() if k != "status"}
            if non_status_changes:
                raise serializers.ValidationError(
                    "Completed tasks cannot be edited. To make changes, first mark the task as Pending."
                )
        return attrs

    def update(self, instance, validated_data):
        old_status = instance.status
        instance = super().update(instance, validated_data)
        # manage completed_at timestamp
        if old_status != instance.status:
            if instance.status == "Completed":
                instance.completed_at = timezone.now()
            elif instance.status == "Pending":
                instance.completed_at = None
            instance.save(update_fields=["completed_at", "status"])
        return instance
