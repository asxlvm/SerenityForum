from django.db import models
import uuid
import time

class UserRole(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(default="#333333", max_length=9)
    numberofusers = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Category(models.Model):
    posts = models.ForeignKey('Post', null = True, on_delete=models.CASCADE)
    numberofposts = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default="A category")
    description = models.CharField(max_length=100, default="The description of a category.")
    icon = models.URLField(max_length=200, default="https://uxwing.com/wp-content/themes/uxwing/download/03-editing-user-action/three-horizontal-lines.png")

class Download(models.Model):
    downloadlink = models.URLField(max_length=100)
    def __str__(self):
        return self.downloadlink

class Comment(models.Model):
    author = models.ForeignKey('User', null = False, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default="This is an empty comment.")
    createdat = models.BigIntegerField(default=time.time)

class Post(models.Model):
    author = models.ForeignKey('User', null = False, on_delete=models.CASCADE)
    postid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    comments = models.ForeignKey('Comment', null = True, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    title = models.CharField(max_length=75)
    downloads = models.ForeignKey('Download', null = True, on_delete=models.CASCADE)
    postcategory = models.ForeignKey('Category', null = False, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    createdat = models.BigIntegerField(default=time.time)

class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    userid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    userbio = models.CharField(max_length=500, default="This user has not modified his bio.")
    userupvotes = models.IntegerField(default=0)
    userpfp = models.URLField(max_length=200, default="https://i.pinimg.com/736x/c9/e3/e8/c9e3e810a8066b885ca4e882460785fa.jpg")
    userposts = models.ForeignKey('Post', null = True, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)
    token = models.CharField(max_length=100)
    createdat = models.BigIntegerField(default=time.time)
    role = models.ForeignKey('UserRole', null = False, on_delete=models.CASCADE)
    banned = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(default="255.255.255.255")
    email = models.EmailField(default="your@email.com")

class ReservedUsername(models.Model):
    username = models.CharField(max_length=25, unique=True)
    reservationkey = models.CharField(max_length=25)
    used = models.BooleanField(default=False)
