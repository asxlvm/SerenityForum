from django.http import HttpResponse, HttpRequest, JsonResponse
from django.template import loader
import json
import string
from http import HTTPStatus
from .models import User, UserRole, Post, Comment, Download, Category
import hashlib
from django.views.decorators.csrf import csrf_exempt

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
    ctx = {}
    return HttpResponse(template.render(ctx, request))

def register(request):
    template = loader.get_template("SerenityForum/register.html")
    ctx = {}
    return HttpResponse(template.render(ctx, request))

@csrf_exempt
def getuser(request, username):
    # token = request.session["token"]
    user = User.objects.filter(username=username)
    # if user.

@csrf_exempt
def getmyself(request):
    token = request.session["token"]

@csrf_exempt
def loginapi(request):
    if any(request.session.get("token", "")):
        toReturn = {
            "message": "You are already logged in!",
            "status": "ALREADY_LOGGEDIN",
            "token": request.session["token"]
        }
        return JsonResponse(toReturn, status=HTTPStatus.BAD_REQUEST)
    bodyJson = json.loads(request.body)
    passwordUnhashed = bodyJson["password"]
    username = bodyJson["username"]
    users = User.objects.filter(username=username)
    if len(users) == 0:
        toReturn = {
            "message": "This user does not exist",
            "status": "USER_NOT_FOUND"
        }
        return JsonResponse(toReturn, status=HTTPStatus.NOT_FOUND)
    user = users[0]
    password = hashlib.sha256(passwordUnhashed.encode("UTF-8")).hexdigest()
    if user.password != password:
        toReturn = {
            "message": "Incorrect password, try again!",
            "status": "INCORRECT_PASSWD"
        }
        return JsonResponse(toReturn, HTTPStatus.UNAUTHORIZED)
    if user.banned:
        toReturn = {
            "message": "This account has been banned!",
            "status": "ACCOUNT_BANNED"
        }
        return JsonResponse(toReturn, status=HTTPStatus.UNAUTHORIZED)
    toReturn = {
        "message": "Logged in!",
        "status": "SUCCESS",
        "token": user.token
    }
    request.session["token"] = user.token
    return JsonResponse(toReturn, status=HTTPStatus.OK)

@csrf_exempt
def registerapi(request: HttpRequest):
    if any(request.session.get("token", "")):
        toReturn = {
            "message": "You are already logged in!",
            "status": "ALREADY_LOGGEDIN",
            "token": request.session["token"]
        }
        return JsonResponse(toReturn, status=HTTPStatus.BAD_REQUEST)
    bodyJson = json.loads(request.body)
    passwordUnhashed = bodyJson["password"]
    if (len(passwordUnhashed) < 7 or 
        (not any((c in string.digits) for c in passwordUnhashed)) or 
        (not any((c in string.ascii_uppercase) for c in passwordUnhashed)) or 
        (not any((c in r"!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~") for c in passwordUnhashed))):
        toReturn = {
            "message": "Incorrect password! Password needs to have more than 7 characters and needs to contain atleast one number, uppercase character and symbol!",
            "status": "INCORRECT_PASSWD_FORMAT"
        }
        return JsonResponse(toReturn, status=HTTPStatus.BAD_REQUEST)
    username = bodyJson["username"]
    usernameUser = User.objects.filter(username=username)
    if not (c in username for c in string.printable[62:]) or len(username) <= 2:
        toReturn = {
            "message": "A username cannot contain special characters and needs to be atleast 3 characters!",
            "status": "INCORRECT_USERNAME_FORMAT"
        }
        return JsonResponse(toReturn, status=HTTPStatus.BAD_REQUEST)
    if len(usernameUser) >= 1:
        toReturn = {
            "message": "This username is taken",
            "status": "USERNAME_TAKEN"
        }
        return JsonResponse(toReturn, status=HTTPStatus.BAD_REQUEST)
    email = bodyJson["email"]
    if len(email.split("@")) != 2:
        toReturn = {
            "message": "Invalid email format, example: your@email.com",
            "status": "INCORRECT_EMAIL_FORMAT"
        }

    ip = get_client_ip(request)
    if len(User.objects.filter(ip=ip)) > 0:
        toReturn = {
            "message": "This IP address is already registered, cannot create an account, contact an administrator on our Discord!",
            "status": "TAKEN_IP"
        }
        return JsonResponse(toReturn, status=HTTPStatus.BAD_REQUEST)
    role = UserRole.objects.filter(name="Registered")[0]
    password = hashlib.sha256(passwordUnhashed.encode("UTF-8")).hexdigest()
    token = hashlib.sha256((username + "." + password).encode("UTF-8")).hexdigest()
    userObj = User(username = username, password = password, token = token, role = role, ip = ip, email = email)
    userObj.save()
    request.session["token"] = token
    toReturn = {
        "message": "Created account!",
        "status": "SUCCESS",
        "token": token
    }
    return JsonResponse(toReturn, status=HTTPStatus.OK)
