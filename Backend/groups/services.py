from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Group, GroupMember

User = get_user_model()

# Group related logic
class GroupService:
    @staticmethod
    @transaction.atomic
    def create_group(name, creator, member_ids=None):
        group = Group.objects.create(name=name, created_by=creator)
        GroupMember.objects.create(group=group, user=creator)

        if member_ids:
            for user_id in member_ids:
                if user_id != creator.id:
                    try:
                        user = User.objects.get(id=user_id)
                        GroupMember.objects.get_or_create(user=user, group=group)
                    except User.DoesNotExist:
                        continue
        return group

    @staticmethod
    def add_group_member(group, user):
        # add mamber to an existing group
        if GroupMember.objects.filter(group=group, user=user).exists():
            raise ValueError("USer is already a member of the group")

        member = GroupMember.objects.create(group=group, user=user)
        return member

    @staticmethod
    def get_user_groups(user):
        # get all groups that a user is a member of
        return Group.objects.filter(members__user=user).distinct().order_by('-created_at')

    @staticmethod
    def is_group_member(group, user):
        # check if a user is a member of a group
        return GroupMember.objects.filter(group=group, user=user).exists()

    @staticmethod
    def get_group_members(group):
        # get all members of a group
        return GroupMember.objects.filter(group=group).select_related("user")

    @staticmethod
    def remove_group_member(group, user):
        # remove a member from a group
        deleted_count, _ = GroupMember.objects.filter(group=group, user=user).delete()
        return deleted_count