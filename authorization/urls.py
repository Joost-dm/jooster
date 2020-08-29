from django.urls import path
from authorization.views import UsersOnline

urlpatterns = [
    path('online/', UsersOnline.as_view())
    ]
