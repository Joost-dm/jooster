from django.urls import path, include
from forum import views

urlpatterns = [

    # Forums API urls.
    path('forum/add/', views.CreateForumView.as_view()),
    path('forum/all/', views.ListForumsView.as_view()),
    path('forum/<int:forum>/', views.ForumDetailsView.as_view()),
    path('forum/<int:forum>/children/', views.ListForumChildren.as_view()),
    path('forum/<int:forum>/membership/<int:user>/', views.ForumMemberView.as_view()),

    # Branches API urls.
    path('branch/add/', views.CreateBranchView.as_view()),
    path('branch/<int:branch>/', views.BranchDetailsView.as_view()),
    path('branch/<int:branch>/children/', views.ListBranchChildren.as_view()),
    path('branch/<int:branch>/membership/<int:user>/', views.BranchMemberView.as_view()),

    # Threads API urls.
    path('thread/add/', views.CreateThreadView.as_view()),
    path('thread/<int:thread>/', views.ThreadDetailsView.as_view()),
    path('thread/<int:thread>/children/', views.ListThreadChildren.as_view()),
    path('thread/<int:thread>/like/', views.ThreadLikeView.as_view()),

    # Posts API urls.
    path('post/add/', views.CreatePostView.as_view()),
    path('post/<int:post>/', views.PostDetailsView.as_view()),
    path('post/<int:post>/like/', views.PostLikeView.as_view()),
]
