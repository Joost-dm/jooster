from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from forum.models import Forum, Branch, Thread, Post, PostLike, ThreadLike, ForumMembership,\
    BranchMembership, PostViewer, ThreadViewer
from authorization.models import CustomUser
from authorization.serializers import UserDetailSerializer


class ForumMembershipSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())
    def create(self, validated_data):
        user = validated_data['user']
        forum = validated_data['forum']
        membership = ForumMembership.objects.create(user=user, forum=forum)
        return membership


class BranchMembershipSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    def create(self, validated_data):
        user = validated_data['user']
        branch = validated_data['branch']
        membership = BranchMembership.objects.create(user=user, branch=branch)
        return membership


class PostLikeSerializer(serializers.Serializer):
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
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Forum
        fields = '__all__'


class BranchCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Branch
        fields = '__all__'


class ThreadCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Thread
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(CustomUser)
    carma = serializers.SerializerMethodField('total_carma')
    users_liked_list = serializers.SerializerMethodField('users_liked')
    users_disliked_list = serializers.SerializerMethodField('users_disliked')

    def users_liked(self, post):
        users = CustomUser.objects.filter(postlike__post=post, postlike__like=True)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def users_disliked(self, post):
        users = CustomUser.objects.filter(postlike__post=post, postlike__like=False)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def total_carma(self, post):
        likes = PostLike.objects.filter(post=post, like=True)
        dislikes = PostLike.objects.filter(post=post, like=False)
        return likes.count() - dislikes.count()

    class Meta:
        model = Post
        fields = ['id', 'author', 'carma', 'users_liked_list', 'users_disliked_list',
                  'text', 'pub_date', 'parent_forum', 'parent_branch', 'parent_thread', 'viewers']


class ThreadDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(CustomUser)
    children_count = serializers.SerializerMethodField('count_children')
    is_unread = serializers.SerializerMethodField('check_unread')
    carma = serializers.SerializerMethodField('total_carma')
    users_liked_list = serializers.SerializerMethodField('users_liked')
    users_disliked_list = serializers.SerializerMethodField('users_disliked')

    def users_liked(self, thread):
        users = CustomUser.objects.filter(threadlike__thread=thread, threadlike__like=True)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def users_disliked(self, thread):
        users = CustomUser.objects.filter(threadlike__thread=thread, threadlike__like=False)
        id_list = []
        for user in users:
            id_list.append(user.id)
        return id_list

    def total_carma(self, thread):
        likes = ThreadLike.objects.filter(thread=thread, like=True)
        dislikes = ThreadLike.objects.filter(thread=thread, like=False)
        return likes.count() - dislikes.count()

    def count_children(self, thread):
        return thread.children.count()

    def check_unread(self, thread):
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
                      'text', 'pub_date', 'parent_forum', 'parent_branch', 'viewers']


class BranchDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(CustomUser)
    children_count = serializers.SerializerMethodField('count_children')
    is_unread = serializers.SerializerMethodField('check_unread')

    def count_children(self, branch):
        return branch.children.count()

    def check_unread(self, branch):
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
    author = UserDetailSerializer(CustomUser)
    children_count = serializers.SerializerMethodField('count_children')

    def count_children(self, forum):
        return forum.children.count()

    class Meta:
            model = Forum
            fields = '__all__'

