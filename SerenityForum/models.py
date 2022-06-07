from django.db import models
import uuid

class UserRole(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(default="#333333", max_length=9)
    numberofusers = models.IntegerField(default=0)

class Category(models.Model):
    posts = models.ForeignKey('Post', null = False, on_delete=models.CASCADE)
    numberofposts = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default="A category")
    description = models.CharField(max_length=100, default="The description of a category.")
    icon = models.URLField(max_length=200, default="https://uxwing.com/wp-content/themes/uxwing/download/03-editing-user-action/three-horizontal-lines.png")

class Download(models.Model):
    downloadlink = models.URLField(max_length=100)

class Comment(models.Model):
    author = models.ForeignKey('User', null = False, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default="This is an empty comment.")

class Post(models.Model):
    author = models.ForeignKey('User', null = False, on_delete=models.CASCADE)
    postid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    comments = models.ForeignKey('Comment', null = False, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    title = models.CharField(max_length=75)
    downloads = models.ForeignKey('Download', null = False, on_delete=models.CASCADE)
    postcategory = models.ForeignKey('Category', null = False, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)

class User(models.Model):
    username = models.CharField(max_length=25)
    userid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    userbio = models.CharField(max_length=500, default="This user has not modified his bio.")
    userupvotes = models.IntegerField(default=0)
    userpfp = models.URLField(max_length=200, default="https://i.pinimg.com/736x/c9/e3/e8/c9e3e810a8066b885ca4e882460785fa.jpg")
    userposts = models.ForeignKey('Post', null = False, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)
    token = models.CharField(max_length=100)
    role = models.ForeignKey('UserRole', null = False, on_delete=models.CASCADE)
    banned = models.BooleanField(default=False)
