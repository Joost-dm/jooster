from django.urls import path
from authorization.views import UserDetailsView, UsersOnline

urlpatterns = [
    path('user/<int:id>/', UserDetailsView.as_view()),
    path('online/', UsersOnline.as_view())
    ]
