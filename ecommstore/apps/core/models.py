from __future__ import unicode_literals

from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser

from io import BytesIO
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_consumer = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="profile_pics", default="defaul.jpg")
    is_admin = False

    class Meta:
        ordering = ['-username']

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__ (self):
        return self.title
