from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from holidays.models import Package
from .contexts import booking_details
import datetime
from decimal import Decimal

def booking(request):
    return render(request, 'booking/booking.html') 

@require_POST
def add_booking(request, holiday_id):
    guests = int(request.POST.get('guests'))
    booking = request.session.get('booking', {})
    booking['holiday_id'] = holiday_id
    booking['guests'] = guests
    booking['departure_airport'] = request.POST.get('departure_airport')
    booking['departure_date'] = request.POST.get('departure_date')
    request.session['booking'] = booking

    return redirect(reverse('booking'))

@require_POST
def update_guests(request):
    booking = request.session.get('booking')
    guests = int(request.POST.get('guests'))
    date = datetime.datetime.now()
    holiday = Package.objects.get(pk=booking['holiday_id'], price__start_date__lte=date, price__end_date__gte=date)
    booking['guests'] = guests
    request.session['booking'] = booking
    subtotal = Decimal(holiday.price_set.all()[0].price * booking['guests'])
    total = subtotal

    return JsonResponse({'success': True, 'subtotal': subtotal, 'total': total})



