from django.urls import path
from . import views

app_name = "comeback"

urlpatterns = [
    path('', views.comeback_main, name='comeback_main')
]
