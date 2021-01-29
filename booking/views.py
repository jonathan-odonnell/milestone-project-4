from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.decorators.http import require_POST

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
    booking['guests'] = guests
    request.session['booking'] = booking
    print(booking)

    return HttpResponse(status=200)



