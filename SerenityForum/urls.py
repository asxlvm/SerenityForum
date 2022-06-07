from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path("categories/<str:categoryname>", views.categoryview)
]
