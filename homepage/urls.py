from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),     # <-- esta línea maneja la raíz "/"
    path("index/", views.index, name="index"),
]