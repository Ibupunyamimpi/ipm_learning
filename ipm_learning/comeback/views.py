from django.shortcuts import render
from datetime import date
from django.conf import settings
from django.contrib import messages
from .models import ComebackJourney, ComebackRecord
from ipm_learning.order.models import OrderItem
from ipm_learning.order.utils import get_or_set_order_session
from django.shortcuts import get_object_or_404, redirect, reverse

def comeback_main(request):
    journey = ComebackJourney.objects.filter(is_active=True).first()
    registration = False
    current_date = date.today()
    
    if journey and journey.signup_start_date <= current_date <= journey.signup_end_date:
        registration = True
    
    context = {
        'journey': journey,
        'registration': registration
    }
    
    if request.method == 'POST':
        order = get_or_set_order_session(request)
        
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            if request.POST.get('pmt_type') == 'monthly':
                is_monthly_pmt = True
            else:
                is_monthly_pmt = False
                
            comeback_record = ComebackRecord.objects.filter(comeback=journey, user=request.user).first()
            
            if comeback_record and comeback_record.is_active:
                messages.info(request, "This item is already in your library")
                return redirect("content:course-library")
            else:
                if comeback_record:
                    comeback_record.delete()
                comeback_record = ComebackRecord.objects.create(
                user = request.user,
                comeback = journey,
                is_monthly_pmt = is_monthly_pmt,
                one_time_price = journey.one_time_price,
                monthly_price = journey.monthly_price,
                num_monthly_pmts = journey.num_monthly_pmts,   
            )
        
            item_filter_lst = order.order_items.filter(comeback_record=comeback_record)
            
            if not item_filter_lst.exists():
                new_item = OrderItem.objects.create(
                    comeback_record = comeback_record,
                    order = order,
                    tickets = 1,
                )
                return redirect("order:summary")
            else:
                messages.info(request, "This item is already in your cart")
                return redirect("order:summary") 
    
    return render(request, 'comeback/comeback_main.html', context)