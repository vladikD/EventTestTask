from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Event, EventRegistration
from .serializers import EventSerializer, RegisterSerializer, LoginSerializer, EventRegistrationSerializer


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={201: 'User registered successfully', 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Authenticate a user and get a token",
        request_body=LoginSerializer,
        responses={200: openapi.Response('Token response', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                'access': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )), 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.save()
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

class EventRegistrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Register a user for an event and send a confirmation email.",
        request_body=EventRegistrationSerializer,
        responses={
            201: "Event registered successfully.",
            400: "Bad Request",
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = EventRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            registration = serializer.save()

            # Відправка email-повідомлення
            user_email = request.user.email
            event = registration.event
            send_mail(
                subject=f'Успішна реєстрація на подію: {event.title}',
                message=f'Ви успішно зареєструвалися на подію "{event.title}", яка відбудеться {event.date} в {event.location}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )

            return Response({"detail": "Event registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all events a user is registered for",
        responses={200: openapi.Response('List of user registrations', EventRegistrationSerializer(many=True))}
    )
    def get(self, request, *args, **kwargs):
        registrations = EventRegistration.objects.filter(user=request.user)
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a list of events",
        responses={200: openapi.Response('List of events', EventSerializer(many=True))}
    )
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new event",
        request_body=EventSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific event",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Event details', EventSerializer)}
    )
    def get(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of a specific event",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=EventSerializer,
        responses={200: 'Updated', 400: 'Bad Request'}
    )
    def put(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific event",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER),
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Поля для фільтрації
    filterset_fields = ['title', 'date', 'location']

    # Поля для пошуку
    search_fields = ['title', 'description', 'location']

    # Порядок сортування
    ordering_fields = ['date', 'title']

    @swagger_auto_schema(
        operation_description="Search and filter events by title, date, or location.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by title or description",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by event title", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filter by event date", type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY, description="Filter by event location",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response('Filtered events', EventSerializer(many=True))}
    )
    def get(self, request, format=None):
        return super().get(request)