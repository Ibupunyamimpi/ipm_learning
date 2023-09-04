from django.shortcuts import render
from datetime import date
from .models import ComebackJourney

def comeback_main(request):
    journey = ComebackJourney.objects.filter(is_active=True).first()
    
    # Get the current date
    current_date = date.today()

    # Default registration status to False
    registration = False

    # Check if journey exists and the current date falls within the registration window
    if journey and journey.signup_start_date <= current_date <= journey.signup_end_date:
        registration = True
    
    context = {
        'journey': journey,
        'registration': registration
    }
    return render(request, 'comeback/comeback_main.html', context)