from django.urls import path, include
from django.shortcuts import render
from forum import views

def index(request):
    return render(request, 'forum/index.html')

urlpatterns = [
    path('forum/<int:forum>/membership/<int:user>/', views.ForumMemberView.as_view()), #Post - add, DELETE - remove
    path('branch/<int:branch>/membership/<int:user>/', views.BranchMemberView.as_view()),

    path('post/<int:post>/like/', views.PostLikeView.as_view()),
    path('thread/<int:thread>/like/', views.ThreadLikeView.as_view()),

    path('', index),
    path('forum/add/', views.CreateForumView.as_view()),
    path('branch/add/', views.CreateBranchView.as_view()),
    path('thread/add/', views.CreateThreadView.as_view()),
    path('post/add/', views.CreatePostView.as_view()),

    path('forum/all/', views.ListForumsView.as_view()),
    path('branch/all/', views.ListBranchesView.as_view()),
    path('thread/all/', views.ListPostsView.as_view()),
    path('post/all/', views.ListPostsView.as_view()),

    path('forum/<int:forum>/', views.ForumDetailsView.as_view()),
    path('branch/<int:branch>/', views.BranchDetailsView.as_view()),
    path('thread/<int:thread>/', views.ThreadDetailsView.as_view()),
    path('post/<int:post>/', views.PostDetailsView.as_view()),

    path('thread/latest/<int:key>/', views.ListPostsView.as_view()),
    path('post/latest/<int:key>/', views.ListPostsView.as_view()),

    path('forum/<int:forum>/children/', views.ListForumChildren.as_view()),
    path('branch/<int:branch>/children/', views.ListBranchChildren.as_view()),
    path('thread/<int:thread>/children/', views.ListThreadChildren.as_view()),
]