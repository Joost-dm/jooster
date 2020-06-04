from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from forum.models import Forum, Branch, Thread, Post, PostLike, ThreadLike, ForumMembership,\
    BranchMembership, PostViewer, ThreadViewer
from authorization.models import CustomUser


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
    def create(self, validated_data):
        user = validated_data['user']
        post = validated_data['post']
        like = PostLike.objects.create(user=user, post=post)
        return like


class ThreadLikeSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())
    def create(self, validated_data):
        user = validated_data['user']
        thread = validated_data['thread']
        like = ThreadLike.objects.create(user=user, thread=thread)
        return like


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
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ThreadDetailSerializer(serializers.ModelSerializer):
    children_count = serializers.SerializerMethodField('count_children')
    is_unread = serializers.SerializerMethodField('check_unread')
    def count_children(self, thread):
        return thread.children.count()

    def check_unread(self, thread):
        posts = thread.children.all()
        user = self.context['request'].user
        unread_counter = 0
        for post in posts:
            try:
                PostViewer.objects.get(user = user, post=post)
            except ObjectDoesNotExist:
                unread_counter += 1
        return unread_counter

    class Meta:
            model = Thread
            fields = '__all__'


class BranchDetailSerializer(serializers.ModelSerializer):
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
    children_count = serializers.SerializerMethodField('count_children')

    def count_children(self, forum):
        return forum.children.count()

    class Meta:
            model = Forum
            fields = '__all__'

