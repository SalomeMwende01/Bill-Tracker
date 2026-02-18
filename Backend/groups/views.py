from rest_framework import status
from rest_framework.views. import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Group
from .serializers import (
    GroupSerializer,
    GroupCreateSerializer,
    AddMemberSerializer
)
from .services import GroupService
from core.exceptions import success_response, error_response

User = get_user_model()

# Create your views here.
# Endpoint for listing and creating groups
class GroupListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get all groups that the current user is a member of
        groups = GroupService.get_user_groups(request.user)
        serializer = GroupCreateSerializer(groups, many=True)

        return success_response(
            data=serializer.data,
            message="Groups retrieved successfully",
        )

    def post(self, request):
        # Create new group
        serializer = GroupCreateSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data["name"]
            member_ids = serializer.validated_data["member_ids"]

            try:
                group = GroupService.create_group(name=name, creator=request.user, member_ids=member_ids)

                response_serializer = GroupSerializer(group)
                return success_response(data=response_serializer.data, message="Group created successfully", status_code=status.HTTP_201_CREATED)
            except Exception as e:
                return error_response(
                    message="Failed to create group",
                    details=str(e),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return error_response(
            message="Invalid input",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


# Endpoint for group details
class GroupDetailView(APIView):
    # GET /api/groups/{id} - get group details
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # get details of specific group
        group = get_object_or_404(Group, pk=pk)

        if not GroupService.is_group_member(request.user, group):
            return error_response(
                message="You are not a member of the group",
                status_code=status.HTTP_403_FORBIDDEN
            )
        serializer = GroupSerializer(group)
        return success_response(
            data=serializer.data,
            message="Group retrieved successfully",
        )

# Endpoint for adding members to a group
class AddGroupMemberView(APIView):
    # POST /api/groups/{id}/members/
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)

        if not GroupService.is_group_member(request.user, group):
            return error_response(
                message="You are not a member of the group",
                status_code=status.HTTP_403_FORBIDDEN
            )
        serializer = AddMemberSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]

            try:
                user = User.objects.get(id=user_id)
                GroupService.add_group_member(request.user, user)

                response_serializer = GroupSerializer(group)
                return success_response(data=response_serializer.data, message="Member added successfully", status_code=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return error_response(
                    message="User not found",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            except ValueError as e:
                return error_response(
                    message=str(e),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        return error_response(
            message="Invalid input",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )



