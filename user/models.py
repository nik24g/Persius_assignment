from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.deletion import CASCADE
from .managers import CustomUserManager
# Create your models here.


class User(AbstractUser):
    username = None
    # Id = models.AutoField
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=50, default="")
    address = models.TextField(default="")
    image = models.ImageField(upload_to ='user/images', null = True, blank = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomUserManager()

    def __str__(self):
        return self.email

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    image = models.ImageField(upload_to ='post/images', null = True, blank = True)
    dsc = models.CharField(max_length=500)
    winner = models.CharField(max_length=100, null = True, blank = True)

    def __str__(self):
        return self.dsc
    pass

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="post")
    comment_user = models.ForeignKey(User, on_delete=CASCADE, related_name="comment_user")
    comment = models.CharField(max_length=100)

    def __str__(self):
        return self.comment_user.email