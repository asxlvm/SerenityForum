from django.contrib import admin

# Register your models here.
from .models import User, UserRole, Post, Comment, Download, Category, ReservedUsername

for Model in [User, UserRole, Post, Comment, Download, Category, ReservedUsername]:
    admin.site.register(Model)