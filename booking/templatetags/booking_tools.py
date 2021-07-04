from django import template


register = template.Library()


@register.filter(name='duration')
def duration(td):
    """
    A template tag to return the flight duration. Code is from
    https://stackoverflow.com/questions/33105457/display-and-format-django-durationfield-in-template
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f'{hours}h {minutes}m'


@register.filter(name='extra_days')
def extra_days(flight):
    """
    A template tag to return the number of extra days. Code is from
    https://pypi.org/project/pytz/ and
    https://stackoverflow.com/questions/151199/how-to-calculate-number-of-days-between-two-given-dates
    """
    departure = flight.origin_time_zone.normalize(
        flight.departure_time.astimezone(flight.origin_time_zone)
    )
    arrival = flight.destination_time_zone.normalize(
        flight.arrival_time.astimezone(flight.destination_time_zone)
    )
    difference = arrival.date() - departure.date()

    if difference.days == 1:
        return f'(+ {difference.days} day)'

    if difference.days > 1:
        return f'(+ {difference.days} days)'


@register.filter(name='extra_quantity')
def extra_quantity(extras, extra_id):
    """
    A template tag to return the extra quantity
    """
    for item in extras:
        if item.extra.id == extra_id:
            return item.quantity
    return 1
