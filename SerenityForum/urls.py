from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path("categories/<str:categoryname>/", views.categoryview),
    path("login/", views.login),
    path("signup/", views.register),
    path("post/<str:postid>/", views.showpost),
    path("api/register/", views.registerapi),
    path("api/login/", views.loginapi),
    path("api/getuser/<str:username>/", views.getuser),
    path("api/selfinfo/", views.getmyself)
]
