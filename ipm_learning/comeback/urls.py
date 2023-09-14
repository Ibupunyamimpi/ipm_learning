from django.urls import path
from .views import comeback_main, ComebackJourneyDetail

app_name = "comeback"

urlpatterns = [
    path('', comeback_main, name='comeback_main'),
    path('<slug:slug>/', ComebackJourneyDetail.as_view(), name='comeback_detail'),
]
