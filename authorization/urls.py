from django.urls import path
from authorization.views import SetAvatar, UserDetailsView, UsersOnline

urlpatterns = [
    path('user/<int:id>/', UserDetailsView.as_view()),
    path('avatar/', SetAvatar.as_view()),
    path('online/', UsersOnline.as_view())
    ]
