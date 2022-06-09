from django.http import HttpResponse, HttpRequest, JsonResponse
from django.template import loader
import json
from .models import User, UserRole, Post, Comment, Download, Category
import hashlib

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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

def login(request):
    template = loader.get_template("SerenityForum/login.html")
    return HttpResponse(template.render(request))

def register(request):
    template = loader.get_template("SerenityForum/register.html")
    return HttpResponse(template.render(request))

def registerapi(request: HttpRequest):
    bodyJson = json.loads(request.body)
    passwordUnhashed = bodyJson["password"]
    username = bodyJson["username"]
    email = bodyJson["email"]
    ip = get_client_ip(request)
    role = UserRole.objects.filter(name="Registered")[0]
    password = hashlib.sha256(passwordUnhashed.encode("UTF-8")).hexdigest()
    token = hashlib.sha256((username + "." + password).encode("UTF-8")).hexdigest()
    userObj = User(username = username, password = password, token = token, role = role, ip = ip, email = email)
    userObj.save()
    request.session["token"] = token
    toReturn = {
        "message": "Created account!",
        "status": "success",
        "token": token
    }
    return JsonResponse(toReturn)
