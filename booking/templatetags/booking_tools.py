from django import template


register = template.Library()


@register.filter(name='duration')
def duration(td):
    #https://stackoverflow.com/questions/33105457/display-and-format-django-durationfield-in-template
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f'{hours}h {minutes}m'


@register.filter(name='next_day')
def next_day(flight):
    departure = flight.departure_time.astimezone(flight.origin_time_zone)
    arrival = flight.arrival_time.astimezone(flight.destination_time_zone)
    difference = arrival.date() - departure.date()

    if difference.days == 1:
        return f'(+ {difference.days} day)'

    if difference.days > 1:
        return f'(+ {difference.days} days)'


@register.filter(name='extra_quantity')
def extra_quantity(extras, item_id):
    for item in extras:
        if item.extra.id == item_id:
            return item.quantity
    return 1
