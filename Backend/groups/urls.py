from django.urls import path
from .views import GroupListCreateView, GroupDetailView, AddGroupMemberView

app_name = 'groups'

urlpatterns = [
    path('', GroupListCreateView.as_view(), name='group-list-create'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('<int:pk>/members/>', AddGroupMemberView.as_view(), name='add-member'),
]