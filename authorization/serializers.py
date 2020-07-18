from rest_framework import serializers
from authorization.models import CustomUser
from forum.models import Post, Thread, PostLike, ThreadLike


class UserDetailSerializer(serializers.ModelSerializer):

    messages_count = serializers.SerializerMethodField('count_messages')
    carma = serializers.SerializerMethodField('user_carma')

    def count_messages(self, user):
        threads_count = Thread.objects.filter(author=user).count()
        posts_count = Post.objects.filter(author=user).count()
        return threads_count + posts_count

    def user_carma(self, user):
        user_threads_liked = ThreadLike.objects.filter(thread__author=user, like=True).count()
        user_threads_disliked = ThreadLike.objects.filter(thread__author=user, like=False).count()
        user_posts_liked = PostLike.objects.filter(post__author=user, like=True).count()
        user_posts_disliked = PostLike.objects.filter(post__author=user, like=False).count()
        return user_threads_liked - user_threads_disliked + user_posts_liked - user_posts_disliked

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "is_staff", "displayed", "avatar", "messages_count", "carma"]
