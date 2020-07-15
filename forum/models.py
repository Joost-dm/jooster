from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from authorization.models import CustomUser

class Forum(Model):
    title = models.CharField(max_length=30, verbose_name='название', unique=True)
    description = models.TextField(max_length=10000, verbose_name='описание', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    author = models.ForeignKey(CustomUser, verbose_name='Автор', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False, verbose_name='Приватный')
    members = models.ManyToManyField(
        CustomUser,
        through='ForumMembership',
        through_fields=('forum', 'user'),
        related_name='ForumMembership'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'форум'
        verbose_name_plural = 'форумы'

class ForumMembership(Model):
    forum = models.ForeignKey(Forum, verbose_name='форум', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='пользователь', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['forum', 'user']
        verbose_name = 'участники форума'
        verbose_name_plural = 'участники форумов'

class Branch(Model):
    title = models.CharField(max_length=30, verbose_name='заголовок')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    author = models.ForeignKey(CustomUser, verbose_name='Автор', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False, verbose_name='Приватный')
    parent_forum = models.ForeignKey('Forum', default='1', related_name='children', on_delete=models.CASCADE,
                                     verbose_name='родительский форум')
    members = models.ManyToManyField(
        CustomUser,
        through='BranchMembership',
        through_fields=('branch', 'user'),
        related_name='BranchMembership'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ветка'
        verbose_name_plural = 'ветки'


class BranchMembership(Model):
    branch = models.ForeignKey(Branch, verbose_name='ветка', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='пользователь', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['branch', 'user']
        verbose_name = 'участники ветки'
        verbose_name_plural = 'участники веток'


class Thread(Model):
    text = models.TextField(max_length=10000, verbose_name='текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    author = models.ForeignKey(CustomUser, verbose_name='Автор', on_delete=models.CASCADE)
    parent_forum = models.ForeignKey('Forum', default='1', related_name='children_threads', on_delete=models.CASCADE,
                                     verbose_name='родительский форум')
    parent_branch = models.ForeignKey('Branch', default='1', related_name='children', on_delete=models.CASCADE,
                                     verbose_name='родительская ветка')
    likes = models.ManyToManyField(
        CustomUser,
        through='ThreadLike',
        through_fields=('thread', 'user'),
        related_name='threadLike'
    )
    viewers = models.ManyToManyField(
        CustomUser,
        through='ThreadViewer',
        through_fields=('thread', 'user'),
        related_name='threadViewer'
    )
    def __str__(self):
        if (len(self.text) >= 30):
            return self.text[:30] + '...'
        else:
            return self.text

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'

class ThreadViewer(Model):
    thread = models.ForeignKey(Thread, verbose_name='Тема', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    counter = models.SmallIntegerField(default=0, verbose_name='Счетчик просмотров')
    class Meta:
        unique_together = ['thread', 'user']
        verbose_name = 'просмотр'
        verbose_name_plural = 'просмотры'

class Post(Model):
    text = models.CharField(max_length=10000, verbose_name='текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    author = models.ForeignKey(CustomUser, verbose_name='Автор', on_delete=models.CASCADE)
    parent_thread = models.ForeignKey('Thread', default='1', related_name='children', on_delete=models.CASCADE,
                               verbose_name='родительский элемент')
    parent_forum = models.ForeignKey('Forum', default='1', related_name='children_posts', on_delete=models.CASCADE,
                                     verbose_name='родительский форум')
    parent_branch = models.ForeignKey('Branch', default='1', related_name='children_posts', on_delete=models.CASCADE,
                                      verbose_name='родительская ветка')
    likes = models.ManyToManyField(
        CustomUser,
        through='PostLike',
        through_fields=('post', 'user'),
        related_name='postLike'
    )
    viewers = models.ManyToManyField(
        CustomUser,
        through='PostViewer',
        through_fields=('post', 'user'),
        related_name='viewers'
    )
    def __str__(self):
        if (len(self.text) >= 30):
            return self.text[:30] + '...'
        else:
            return self.text

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class PostViewer(Model):
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    counter = models.SmallIntegerField(default=0, verbose_name='Счетчик просмотров')

    class Meta:
        unique_together = ['post', 'user']
        verbose_name = 'просмотр'
        verbose_name_plural = 'просмотры'

class PostLike(Model):
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    like = models.BooleanField(default= True, verbose_name='Нравится')

    class Meta:
        unique_together = ['post', 'user']
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'

class ThreadLike(Model):
    thread = models.ForeignKey(Thread, verbose_name='Тема', default='1', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', default='1', on_delete=models.CASCADE)
    like = models.BooleanField(default=True, verbose_name='Нравится')

    class Meta:
        unique_together = ['thread', 'user']
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'
