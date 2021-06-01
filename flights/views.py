from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from holidays.utlis import superuser_required
from holidays.models import Flight
from .forms import FlightForm
from .utils import get_flights


def airports(request, holiday_id):
    airports = Flight.objects.filter(packages=holiday_id, direction='Outbound')
    airports = list(airports.values_list('origin', flat=True).distinct())
    return JsonResponse({'airports': airports})


@login_required
@superuser_required
def flights(request):
    flights = get_flights(request)
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sort = request.GET['sort']
        if 'direction' in request.GET:
            direction = request.GET['direction']
    
    current_sorting = f'{sort}_{direction}'
    template = 'flights/flights.html'
    context = {
        'flights': flights,
        'current_sorting': current_sorting,
    }

    return render(request, template, context)


@login_required
@superuser_required
def filter_flights(request):
    flights = get_flights(request)
    html = render_to_string(
        'flights/includes/flights_table.html', {'flights': flights})
    return JsonResponse({'flights': html})

@login_required
@superuser_required
def add_flight(request):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added flight!')
            return redirect(redirect_url or reverse('flights'))
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
    redirect_url = request.POST.get('redirect_url')
    flight = get_object_or_404(Flight, flight_number=flight_number)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated flight!')
            return redirect(redirect_url or reverse('flights'))
        else:
            messages.error(
                request, 'Failed to update flight. Please ensure the form is valid.')
    else:
        form = FlightForm(instance=flight)

    template = 'flights/edit_flight.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
@superuser_required
def delete_flight(request, flight_number):
    flight = get_object_or_404(Flight, name=flight_number)
    flight.delete()
    messages.success(request, 'Flight deleted!')
    return redirect(reverse('Flights'))
