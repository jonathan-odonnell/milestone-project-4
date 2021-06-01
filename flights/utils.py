from .models import Flight
from django.core.paginator import Paginator

def get_flights(request):
    flights = Flight.objects.all()

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

    paginated_flights = Paginator(flights, 10)
    page_number = request.GET.get('page')
    flights = paginated_flights.get_page(page_number)

    return flights
