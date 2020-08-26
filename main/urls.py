from django.urls import path, include, re_path
from django.views.static import serve as _serve


def serve(request, path):
    if "." not in path:
        path = "index.html"
    return _serve(request, path, "./frontend/dist")


def serveIMG(request, path):
    return _serve(request, path, "")


urlpatterns = [
    path("api/v1/", include('forum.urls')),
    path('api/v1/auth/', include('authorization.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    re_path(r"(?P<path>(.+\.(jpg|bmp|png|jpeg|svg)))", serveIMG),
    re_path(r"(?P<path>(^/?$|.+))", serve),
]
