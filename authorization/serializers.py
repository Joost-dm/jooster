from abc import ABC

import redis
from rest_framework import serializers
from authorization.models import CustomUser
from forum.models import Post, Thread, PostLike, ThreadLike
from authorization.validators import DownloadedAvatarValidator
from main.settings import REDIS_SETTINGS


class UserDetailSerializer(serializers.ModelSerializer):
    """ Extended user-model serializer """

    messages_count = serializers.SerializerMethodField('count_messages')
    carma = serializers.SerializerMethodField('user_carma')
    avatar_url = serializers.SerializerMethodField('actual_avatar_url_handler')
    avatar = serializers.ImageField(write_only=True, validators=[DownloadedAvatarValidator])
    is_staff = serializers.BooleanField(read_only=True)

    def count_messages(self, user):
        """ Returns user threads + posts count """

        threads_count = Thread.objects.filter(author=user).count()
        posts_count = Post.objects.filter(author=user).count()
        return threads_count + posts_count

    def user_carma(self, user):
        """ Returns users's current carma value """

        user_threads_liked = ThreadLike.objects.filter(thread__author=user, like=True).count()
        user_threads_disliked = ThreadLike.objects.filter(thread__author=user, like=False).count()
        user_posts_liked = PostLike.objects.filter(post__author=user, like=True).count()
        user_posts_disliked = PostLike.objects.filter(post__author=user, like=False).count()
        return user_threads_liked - user_threads_disliked + user_posts_liked - user_posts_disliked

    def actual_avatar_url_handler(self, user):
        """ Returns prioritized URL to user's avatar.
        The avatar priority is (from max to min):
            1. Downloaded avatar
            2. Foreign avatar (example: from social network account when using social auth)
            3. Default avatar """

        if 'default_avatar.png' in user.avatar.url and user.foreign_avatar_url:
            return user.foreign_avatar_url
        else:
            return user.avatar.url

    class Meta:
        model = CustomUser
        fields = ["id", "email", "is_staff", "displayed", "avatar_url", "messages_count", "carma", "avatar"]


class UsersOnlineSerializer(serializers.Serializer):
    users_online = serializers.ListField(child=UserDetailSerializer())
