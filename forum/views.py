from rest_framework import generics, status
from rest_framework.response import Response
from forum import serializers
from forum.models import Forum, Branch, Thread, Post, PostLike, ThreadLike, ForumMembership,\
    BranchMembership, ThreadViewer, PostViewer
from authorization.models import CustomUser
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from forum import permissions


# todo: permissions
from forum.paginationclasses import StandardResultsSetPagination


class ForumMemberView(generics.GenericAPIView):
    serializer_class = serializers.ForumMembershipSerializer

    def post(self, request, **kwargs):
        data = request.data.copy()
        data.update({'forum': kwargs['forum']})
        data.update({'user': kwargs['user']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
              return Response(data={"user": "already in members"}, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, **kwargs):
        data = request.data.copy()
        data.update({'forum': kwargs['forum']})
        data.update({'user': kwargs['user']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(ForumMembership, forum=kwargs['forum'], user=kwargs['user']).delete()
        return Response(data={"user": "removed"}, status=status.HTTP_204_NO_CONTENT)


# todo: permissions
class BranchMemberView(generics.GenericAPIView):
    serializer_class = serializers.BranchMembershipSerializer

    def post(self, request, **kwargs):
        data = request.data.copy()
        data.update({'branch': kwargs['branch']})
        data.update({'user': kwargs['user']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
              return Response(data={"user": "already in members"}, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, **kwargs):
        data = request.data.copy()
        data.update({'branch': kwargs['branch']})
        data.update({'user': kwargs['user']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(BranchMembership, branch=kwargs['branch'], user=kwargs['user']).delete()
        return Response(data={"user": "removed"}, status=status.HTTP_204_NO_CONTENT)


# todo: permissions
class PostLikeView(generics.GenericAPIView):
    serializer_class = serializers.PostLikeSerializer

    def post(self, request, **kwargs):
        data = request.data.copy()
        data.update({'post': kwargs['post']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
              return Response(data={"post": "already liked"}, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, **kwargs):
        data = request.data.copy()
        data.update({'post': kwargs['post']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(PostLike, post=kwargs['post'], user=request.user).delete()
        return Response(data={"post": "deleted"}, status=status.HTTP_204_NO_CONTENT)


# todo: permissions
class ThreadLikeView(generics.GenericAPIView):
    serializer_class = serializers.ThreadLikeSerializer

    def post(self, request, **kwargs):
        data = request.data.copy()
        data.update({'thread': kwargs['thread']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
              return Response(data={"thread": "already liked"}, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, **kwargs):
        data = request.data.copy()
        data.update({'thread': kwargs['thread']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(ThreadLike, thread=kwargs['thread'], user=request.user).delete()
        return Response(data={"thread": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class CreateForumView(generics.CreateAPIView):
    serializer_class = serializers.ForumCreateSerializer


class CreateBranchView(generics.CreateAPIView):
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin]
    serializer_class = serializers.BranchCreateSerializer


class CreateThreadView(generics.CreateAPIView):
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin]
    serializer_class = serializers.ThreadCreateSerializer
    def post(self, request, *args, **kwargs):
        request.data['parent_forum'] = Branch.objects.get(id=request.data['parent_branch']).parent_forum.id
        return self.create(request, *args, **kwargs)


class CreatePostView(generics.CreateAPIView):
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin]
    serializer_class = serializers.PostCreateSerializer
    def post(self, request, *args, **kwargs):
        request.data['parent_branch'] = Thread.objects.get(id=request.data['parent_thread']).parent_branch.id
        request.data['parent_forum'] = Branch.objects.get(id=request.data['parent_branch']).parent_forum.id
        return self.create(request, *args, **kwargs)


# todo: permissions or delete
class ListForumsView(generics.ListAPIView):
    serializer_class = serializers.ForumDetailSerializer
    def get(self, request, *args, **kwargs):
        self.queryset = Forum.objects.all().order_by('pub_date')
        return self.list(request, *args, **kwargs)


# todo: permissions or delete
class ListBranchesView(generics.ListAPIView):
    serializer_class = serializers.BranchDetailSerializer
    def get(self, request, *args, **kwargs):
        self.queryset = Branch.objects.all().order_by('-pub_date')
        return self.list(request, *args, **kwargs)


# todo: permissions or delete
class ListThreadsView(generics.ListAPIView):
    serializer_class = serializers.ThreadDetailSerializer
    def get(self, request, *args, **kwargs):
        try:
            self.queryset = Thread.objects.all().order_by('-pub_date')[:kwargs['key']]
        except KeyError:
            self.queryset = Thread.objects.all().order_by('-pub_date')
        return self.list(request, *args, **kwargs)


# todo: permissions or delete
class ListPostsView(generics.ListAPIView):
    serializer_class = serializers.PostDetailSerializer
    def get(self, request, *args, **kwargs):
        try:
            self.queryset = Post.objects.all().order_by('-pub_date')[:kwargs['key']]
        except KeyError:
            self.queryset = Post.objects.all().order_by('-pub_date')
        return self.list(request, *args, **kwargs)


class ListForumChildren(generics.ListAPIView):
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin]
    serializer_class = serializers.BranchDetailSerializer
    def get(self, request, *args, **kwargs):
        self.queryset = Branch.objects.all().filter(parent_forum=kwargs['forum'])
        return self.list(request, *args, **kwargs)


class ListBranchChildren(generics.ListAPIView):
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin]
    serializer_class = serializers.ThreadDetailSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request, *args, **kwargs):
        self.queryset = Thread.objects.all().filter(parent_branch=kwargs['branch'])[::-1]
        for thread in self.queryset:
            try:
                ThreadViewer.objects.create(thread=thread ,user=request.user)
            except ValueError:
                pass
            except IntegrityError:
                viewer = ThreadViewer.objects.get(thread=thread ,user=request.user)
                viewer.counter = viewer.counter + 1
                viewer.save()
        return self.list(request, *args, **kwargs)


class ListThreadChildren(generics.ListAPIView):
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin]
    serializer_class = serializers.PostDetailSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request, *args, **kwargs):
        self.queryset = Post.objects.all().filter(parent_thread=kwargs['thread'])[::-1]
        for post in self.queryset:
            try:
                PostViewer.objects.create(post=post ,user=request.user)
            except ValueError:
                pass
            except IntegrityError:
                viewer = PostViewer.objects.get(post=post ,user=request.user)
                viewer.counter = viewer.counter + 1
                viewer.save()
        return self.list(request, *args, **kwargs)


class ForumDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'forum'
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsAuthorOrReadOnlyOrAdmin]
    serializer_class = serializers.ForumDetailSerializer
    queryset = Forum.objects.all()


class BranchDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'branch'
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin,
                          permissions.IsAuthorOrReadOnlyOrAdmin]
    serializer_class = serializers.BranchDetailSerializer
    queryset = Branch.objects.all()


class ThreadDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'thread'
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin,
                          permissions.IsAuthorOrReadOnlyOrAdmin]

    serializer_class = serializers.ThreadDetailSerializer
    queryset = Thread.objects.all()


class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'post'
    permission_classes = [permissions.IsPrivateForumMemberOrAdmin,
                          permissions.IsPrivateBranchMemberOrAdmin,
                          permissions.IsAuthorOrReadOnlyOrAdmin]
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all()