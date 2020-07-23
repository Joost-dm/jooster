""" Forum serializers. """

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from forum.models import Forum, Branch, Thread, Post, PostLike, ThreadLike, ForumMembership,\
    BranchMembership, PostViewer, ThreadViewer
from authorization.models import CustomUser
from authorization.serializers import UserDetailSerializer


class ForumMembershipSerializer(serializers.Serializer):
    """ Forum membership serializer. """

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())
    def create(self, validated_data):
        user = validated_data['user']
        forum = validated_data['forum']
        membership = ForumMembership.objects.create(user=user, forum=forum)
        return membership


class BranchMembershipSerializer(serializers.Serializer):
    """ Branch membership serializer. """

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    def create(self, validated_data):
        user = validated_data['user']
        branch = validated_data['branch']
        membership = BranchMembership.objects.create(user=user, branch=branch)
        return membership


class PostLikeSerializer(serializers.Serializer):
    """ User's opinion about post serializer. """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    like = serializers.BooleanField()
    def create(self, validated_data):
        user = validated_data['user']
        post = validated_data['post']
        like = validated_data['like']
        carma = PostLike.objects.create(user=user, post=post, like=like)
        return carma


class ThreadLikeSerializer(serializers.Serializer):
    """ User's opinion about thread serializer. """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())
    like = serializers.BooleanField()
    def create(self, validated_data):
        user = validated_data['user']
        thread = validated_data['thread']
        like = validated_data['like']
        carma = ThreadLike.objects.create(user=user, thread=thread, like=like)
        return carma


class ForumCreateSerializer(serializers.ModelSerializer):
    """ Forum creation serializer. """

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Forum
        fields = '__all__'


class BranchCreateSerializer(serializers.ModelSerializer):
    """ Branch creation serializer. """

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Branch
        fields = '__all__'


class ThreadCreateSerializer(serializers.ModelSerializer):
    """ Thread creation serializer. """

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Thread
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    """ Post creation serializer. """

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    """ Post details serializer. """

    author = UserDetailSerializer(CustomUser)
    carma = serializers.SerializerMethodField('total_carma')
    users_liked_list = serializers.SerializerMethodField('users_liked')
    users_disliked_list = serializers.SerializerMethodField('users_disliked')

    def users_liked(self, post):
        """ Returns users list with positive opinion of the current post."""
        users = CustomUser.objects.filter(postlike__post=post, postlike__like=True)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def users_disliked(self, post):
        """ Returns users list with negative opinion of the current post."""

        users = CustomUser.objects.filter(postlike__post=post, postlike__like=False)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def total_carma(self, post):
        """ Returns value of current carma of the post. """

        likes = PostLike.objects.filter(post=post, like=True)
        dislikes = PostLike.objects.filter(post=post, like=False)
        return likes.count() - dislikes.count()

    class Meta:
        model = Post
        fields = ['id', 'author', 'carma', 'users_liked_list', 'users_disliked_list',
                  'text', 'pub_date', 'parent_forum', 'parent_branch', 'parent_thread', 'viewers']


class ThreadDetailSerializer(serializers.ModelSerializer):
    """ Thread details serializer. """

    author = UserDetailSerializer(CustomUser)
    children_count = serializers.SerializerMethodField('count_children')
    is_unread = serializers.SerializerMethodField('check_unread')
    carma = serializers.SerializerMethodField('total_carma')
    users_liked_list = serializers.SerializerMethodField('users_liked')
    users_disliked_list = serializers.SerializerMethodField('users_disliked')
    parent_branch_title = serializers.SerializerMethodField('get_parent_branch_title')

    def get_parent_branch_title(self, thread):
        """ Returns the name of the parent branch of this thread. (It's used for creating back-link
         (to the parent branch) from the secondary(thread) window at the interface."""

        return Branch.objects.get(id=thread.parent_branch.id).title

    def users_liked(self, thread):
        """ Returns users list with positive opinion of the current thread."""

        users = CustomUser.objects.filter(threadlike__thread=thread, threadlike__like=True)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def users_disliked(self, thread):
        """ Returns users list with negative opinion of the current post."""

        users = CustomUser.objects.filter(threadlike__thread=thread, threadlike__like=False)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def total_carma(self, thread):
        """ Returns value of current carma of the thread. """

        likes = ThreadLike.objects.filter(thread=thread, like=True)
        dislikes = ThreadLike.objects.filter(thread=thread, like=False)
        return likes.count() - dislikes.count()

    def count_children(self, thread):
        """ Returns the count of thread's children. """

        return thread.children.count()

    def check_unread(self, thread):
        """ Returns count of the unread posts in the thread. """

        posts = thread.children.all()
        user = self.context['request'].user
        unread_counter = 0
        for post in posts:
            try:
                PostViewer.objects.get(user=user, post=post)
            except ObjectDoesNotExist:
                unread_counter += 1
        return unread_counter

    class Meta:
            model = Thread
            fields = ['id', 'author', 'children_count', 'is_unread', 'carma', 'users_liked_list', 'users_disliked_list',
                      'text', 'pub_date', 'parent_forum', 'parent_branch', 'viewers', 'parent_branch_title']


class BranchDetailSerializer(serializers.ModelSerializer):
    """ Branch detail serializer. """

    author = UserDetailSerializer(CustomUser)
    children_count = serializers.SerializerMethodField('count_children')
    is_unread = serializers.SerializerMethodField('check_unread')

    def count_children(self, branch):
        """ Returns the count of branch's children. """

        return branch.children.count()

    def check_unread(self, branch):
        """ Returns the count of unread threads in the branch. """

        threads = branch.children.all()
        user = self.context['request'].user
        unread_counter = 0
        for thread in threads:
            try:
                ThreadViewer.objects.get(user=user, thread=thread)
            except ObjectDoesNotExist:
                unread_counter += 1
        return unread_counter

    class Meta:
        model = Branch
        fields = '__all__'


class ForumDetailSerializer(serializers.ModelSerializer):
    """ Forum detail serializer. """
    author = UserDetailSerializer(CustomUser)
    children_count = serializers.SerializerMethodField('count_children')

    def count_children(self, forum):
        """ Returns the count of the forum's children. """
        
        return forum.children.count()

    class Meta:
            model = Forum
            fields = '__all__'

