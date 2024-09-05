from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Event, EventRegistration

import re



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['event']

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data.get('event')
        return EventRegistration.objects.create(user=user, event=event)

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username is already in use.")
        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise serializers.ValidationError("Username can contain only letters, numbers, and _.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use.")
        return email

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("The password must be at least 8 characters long.")
        if not re.search(r'\d', password):
            raise serializers.ValidationError("The password must contain at least one digit.")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("The password must contain at least one capital letter.")
        return password

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        user.username = self.validated_data['username']
        user.email = self.validated_data['email']
        user.set_password(self.validated_data['password'])
        user.save()
        setup_user_email(request, user, [])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        data['user'] = user
        return data

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def save(self, **kwargs):
        return self.get_token(self.validated_data['user'])
