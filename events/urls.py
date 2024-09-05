from django.urls import path
from .views import EventListView, EventDetailView, RegisterView, LoginView, CustomTokenObtainPairView, \
    CustomTokenRefreshView, EventRegistrationView, UserRegistrationsView

urlpatterns = [
    #методом GET отримаємо всі події, методом POST зареєструємо подію
    path('events/', EventListView.as_view(), name='event-list'),
    #методом GET отримуємо всі події на які зареєстрований клристувач
    path('events/registrations/', UserRegistrationsView.as_view(), name='user-registrations'),
    #методом GET отримуємо інфориацію про певну поді.
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    #методом POST реєструємось на подію
    path('events/register/', EventRegistrationView.as_view(), name='event_register'),
    #реєстрація користувача
    path('register/', RegisterView.as_view(), name='register'),
    #автризація
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
