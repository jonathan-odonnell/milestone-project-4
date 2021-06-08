from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from holidays.utlis import superuser_required
from holidays.models import Flight
from .forms import FlightForm


def airports(request, holiday_id):
    """
    A view to return a list of all outbound airports. Code for returning
    distinct airport names in a list is from
    https://stackoverflow.com/questions/10848809/django-model-get-distinct-value-list
    """
    airports = Flight.objects.filter(packages=holiday_id, direction='Outbound')
    airports = list(airports.values_list('origin', flat=True).distinct())
    return JsonResponse({'airports': airports})


@login_required
@superuser_required
def flights(request):
    """
    A view to show filghts including sorting and pagination. Code for
    pagination is from https://docs.djangoproject.com/en/3.2/topics/pagination/
    and code for processing JSON requests is from
    https://stackoverflow.com/questions/8587693/django-request-is-ajax-returning-false
    and the code for rendering the flight_table template to a string is from
    https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
    """
    flights = Flight.objects.all()
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'number':
                sort = 'flight_number'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort = f'-{sort}'
                flights = flights.order_by(sort)

    current_sorting = f'{sort}_{direction}'
    paginated_flights = Paginator(flights, 10)
    page_number = request.GET.get('page')
    flights = paginated_flights.get_page(page_number)

    if request.is_ajax():
        flights_html = render_to_string(
            'flights/includes/flights_table.html', {'flights': flights})
        return JsonResponse({'flights': flights_html})

    template = 'flights/flights.html'
    context = {
        'flights': flights,
        'current_sorting': current_sorting,
    }

    return render(request, template, context)


@login_required
@superuser_required
def add_flight(request):
    """
    A view to display the add flight page and add the flight to the database.
    """
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added flight!')
            return redirect(redirect_url or reverse('flights'))
        else:
            messages.error(
                request,
                'Failed to add flight. Please ensure the form is valid.')
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
    """
    A view to display the edit flight page and update the flight
    in the database.
    """
    flight = get_object_or_404(Flight, flight_number=flight_number)
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated flight!')
            return redirect(redirect_url or reverse('flights'))
        else:
            messages.error(
                request,
                'Failed to update flight. Please ensure the form is valid.')
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
    """
    A view to delete the flight from the database. Code for the redirect_url
    is from
    https://stackoverflow.com/questions/27325505/django-getting-previous-url
    """
    redirect_url = request.META.get('HTTP_REFERRER')
    flight = get_object_or_404(Flight, flight_number=flight_number)
    flight.delete()
    messages.success(request, 'Flight deleted!')
    return redirect(redirect_url or reverse('flights'))
