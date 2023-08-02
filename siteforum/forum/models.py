from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Categories(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    slug = models.SlugField(
        max_length=255, db_index=True, unique=True, verbose_name="URL"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})


class Posts(models.Model):
    title = models.CharField(max_length=250, null=True, verbose_name="заголовок поста")
    content = models.TextField(verbose_name="содержание поста", blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="время создания")
    update_time = models.DateTimeField(
        auto_now=True, verbose_name="время редактирования"
    )
    author = models.ForeignKey('Users', on_delete=models.PROTECT, verbose_name="автор")
    cat = models.ForeignKey(
        Categories, on_delete=models.PROTECT, verbose_name="категория"
    )
    likes = models.ManyToManyField(Users, blank=True, related_name='liked_posts')
    dislikes = models.ManyToManyField(Users, blank=True, related_name='disliked_posts')
    views = models.ManyToManyField(Users, blank=True, related_name='viewed_posts')
    is_published = models.BooleanField(default=True, verbose_name="публикация")
    is_allow_comments = models.BooleanField(verbose_name="разрешить комментарии")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comments(models.Model):
    content = models.TextField(verbose_name="содержание комментария")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="время создания")
    update_time = models.DateTimeField(
        auto_now=True, verbose_name="время редактирования"
    )
    author = models.ForeignKey(
        'Users',
        on_delete=models.PROTECT,
        verbose_name="автор",
        related_name="comments_written",
    )
    recipient = models.ForeignKey(
        'Users',
        on_delete=models.PROTECT,
        related_name="comments_received",
        verbose_name="адресат",
    )
    post = models.ForeignKey(
        'Posts',
        on_delete=models.PROTECT,
        verbose_name="пост",
        related_name="comments_post",
    )
    likes = models.ManyToManyField(Users, blank=True, related_name='liked_comments')
    dislikes = models.ManyToManyField(Users, blank=True, related_name='disliked_comments')
    is_approved = models.BooleanField(default=True, verbose_name="модерация")

    def __str__(self):
        return "автор: " + str(self.author.username) + ", пост: " + str(self.post)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"