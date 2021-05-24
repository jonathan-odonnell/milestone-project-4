from django import template
from pytz import timezone


register = template.Library()


@register.filter(name='duration')
def duration(td):
    #https://stackoverflow.com/questions/33105457/display-and-format-django-durationfield-in-template
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f'{hours}h {minutes}m'


@register.simple_tag(name='next_day')
def next_day(flight, time_zone, direction):
    # https://www.w3resource.com/python-exercises/python-basic-exercise-14.php
    # https://pypi.org/project/pytz/
    # https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#writing-custom-template-filters

    time_zone = timezone(time_zone)
    departure = flight.departure_time
    arrival = flight.arrival_time

    if direction == 'outbound':
        arrival = arrival.astimezone(time_zone)
    
    else:
        departure = departure.astimezone(time_zone)

    difference = arrival.date() - departure.date()

    if difference.days > 0:
        return f'(+ {difference.days} day)'

@register.filter(name='extra_quantity')
def extra_quantity(extras, item_id):
    for item in extras:
        if item.extra.id == item_id:
            return item.quantity
    return 1
