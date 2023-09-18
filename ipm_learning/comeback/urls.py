from django.urls import path
from .views import comeback_main, ComebackJourneyDetail, add_to_waitlist_view

app_name = "comeback"

urlpatterns = [
    path('', comeback_main, name='comeback_main'),
    path('add_to_waitlist/', add_to_waitlist_view, name='add_to_waitlist'),
    path('<slug:slug>/', ComebackJourneyDetail.as_view(), name='comeback_detail'),
]
