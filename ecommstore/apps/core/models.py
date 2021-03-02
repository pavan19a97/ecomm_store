from __future__ import unicode_literals
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser


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

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null= True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='product_pics', blank=True, null = True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'http://via.polaceholder.com/240*180.jpg'

    def make_thumbnail(self, image, size = (300, 200)):
        img = Image.open(image)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality =85)

        thumbnail = File(thumb_io, name= image.name)
        return thumbnail
