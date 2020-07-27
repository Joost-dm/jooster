from django.urls import path
from authorization.views import SetAvatar, UserDetailsView

urlpatterns = [
    path('users/<int:id>/', UserDetailsView.as_view()),
    path('avatar/', SetAvatar.as_view()),
    ]
