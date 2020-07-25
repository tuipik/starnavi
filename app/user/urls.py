from django.urls import path
from .views import (UserRegistrationView,
                    UserLoginView,
                    UserProfileView,
                    UserAnaliticsView
                    )

app_name = 'user'

urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('signin/', UserLoginView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('analitics/', UserAnaliticsView.as_view()),
    ]
