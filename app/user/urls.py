from django.urls import path
from .views import (UserRegistrationView,
                    UserLoginView,
                    UserProfileView,
                    UserAnaliticsView
                    )

app_name = 'user'

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='signin'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('analitics/', UserAnaliticsView.as_view(), name='analitics'),
    ]
