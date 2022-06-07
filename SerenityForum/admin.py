from django.contrib import admin

# Register your models here.
from .models import User, UserRole, Post, Comment, Download, Category

for Model in [User, UserRole, Post, Comment, Download, Category]:
    admin.site.register(Model)