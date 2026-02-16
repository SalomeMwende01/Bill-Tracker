from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer
from core.exceptions import success_response, error_response


# Create your views here.

# Endpoint for user registration
class UserRegistrationView(APIView):
    # POST /api/auth/register
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # generate JWT token
            refresh = RefreshToken.for_user(user)

            return success_response(
                data={
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                message='User registered successfully',
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message='Registration failed',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


# Endpoint for user login
class UserLoginView(APIView):
    # POST /api/auth/login
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                return success_response(
                    data={
                        'user': UserSerializer(user).data,
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    message='Login successful',
                )
            else:
                return error_response(
                    message='invalid credentials',
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        return error_response(
            message='Invalid input',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Endpoint for current user
class CurrentUserView(APIView):
    # GET /api/auth/me
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(
            data=serializer.data,
            message="user retrieved succcessful"
        )