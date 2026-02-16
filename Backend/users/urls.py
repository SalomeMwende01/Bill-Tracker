from django.urls import path
from .views import UserRegistrationView, UserLoginView, CurrentUserView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
]