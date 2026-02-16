from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'password_confirm')
        read_only_fields = ('id',)

        def validate(self, attrs):
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError({"password": "Passwords fields didn't match"})
            return attrs

        def create(self, validated_data):
            validated_data.pop('password_confirm')
            user = User.objects.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                password=validated_data['password']
            )
            return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
        read_only_fields = ('id', 'name', 'email')