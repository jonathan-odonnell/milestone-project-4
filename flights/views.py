from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from holidays.utlis import superuser_required
from holidays.models import Flight
from .forms import FlightForm


@login_required
@superuser_required
def flights(request):
    flights = Flight.objects.all()
    paginated_flights = Paginator(flights, 10)
    page_number = request.GET.get('page')
    flights = paginated_flights.get_page(page_number)

    context = {
        'flights': flights,
    }

    return render(request, 'flights/flights.html', context)


@login_required
@superuser_required
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added flight!')
            return redirect(reverse('flights'))
        else:
            messages.error(
                request, 'Failed to add flight. Please ensure the form is valid.')
    else:
        form = FlightForm()

    template = 'flights/add_flight.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
@superuser_required
def edit_flight(request, flight_number):
    flight = get_object_or_404(Flight, name=flight_number)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated flight!')
            return redirect(reverse('flights'))
        else:
            messages.error(
                request, 'Failed to update flight. Please ensure the form is valid.')
    else:
        form = FlightForm(instance=flight)

    template = 'flights/edit_flight.html'
    context = {
        'form': form,
        'flight': flight,
    }

    return render(request, template, context)


@login_required
@superuser_required
def delete_flight(request, flight_number):
    flight = get_object_or_404(Flight, name=flight_number)
    flight.delete()
    messages.success(request, 'Flight deleted!')
    return redirect(reverse('Flights'))
