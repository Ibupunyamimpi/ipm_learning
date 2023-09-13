from django.urls import path
from .views import comeback_main, ComebackDetail

app_name = "comeback"

urlpatterns = [
    path('', comeback_main, name='comeback_main'),
    path('<int:pk>/', ComebackDetail.as_view(), name='comeback_detail'),
]
