from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from holidays.utlis import superuser_required
from holidays.models import Flight
from .forms import FlightForm


@login_required
@superuser_required
def flights(request):
    flights = Flights.objects.all()

    context = {
        'flights': flights,
    }

    return render(request, 'flights/flights.html', context)


@login_required
@superuser_required
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES)
        if form.is_valid():
            flight = form.save()
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
        form = FlightForm(request.POST, request.FILES, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated flight!')
            return redirect(reverse('flights'))
        else:
            messages.error(
                request, 'Failed to update flight. Please ensure the form is valid.')

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
