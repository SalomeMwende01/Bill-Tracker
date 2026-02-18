from rest_framework import serializers
from .models import Group, GroupMember
from app.users.serializers import UserMinimalSerializer


# Serializer for group members
class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ('id', 'user', 'joined_at')
        read_only_fields = ('id', 'joined_at')

# Serializer for group model with members
class GroupSerializer(serializers.ModelSerializer):
    created_at = UserMinimalSerializer(read_only=True)
    members = GroupMemberSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'created_by', 'members', 'members_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def get_members_count(self, obj):
        return obj.members.count()

# Serializer for creating a new group
class GroupCreateSerializer(serializers.ModelSerializer):
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of user IDs to add as members."
    )

    class Meta:
        model = Group
        fields = ('id', 'name', 'member_ids')
        read_only_fields = ('id',)

# Serializer for adding a member to a group
class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True, help_text="ID of the user to add")

    def validate_user_id(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
