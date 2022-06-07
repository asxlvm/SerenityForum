from django.http import HttpResponse
from django.template import loader
from .models import User, UserRole, Post, Comment, Download, Category

def home(request):
    categories = Category.objects.all()
    template = loader.get_template("SerenityForum/home.html")
    ctx = {
        "categories": categories,
    }
    return HttpResponse(template.render(ctx, request))

def categoryview(request, categoryname):
    category = Category.objects.filter(title=categoryname)[0]
    template = loader.get_template("SerenityForum/categories.html")
    ctx = {
        "category": category,
        "posts": Post.objects.filter(postcategory=category)
    }
    return HttpResponse(template.render(ctx, request))