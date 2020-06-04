from django.urls import path
from authorization.views import SetAvatar

urlpatterns = [
    path('avatar/', SetAvatar.as_view()),
    ]
