from django import template


register = template.Library()


@register.filter(name='duration')
def duration(td):
    #https://stackoverflow.com/questions/33105457/display-and-format-django-durationfield-in-template
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{}h {}m'.format(hours, minutes)


@register.filter(name='next_day')
def next_day(flight):
    departure = flight.departure_time.date()
    arrival = flight.arrival_time.date()
    difference = arrival - departure

    return difference.days

@register.filter(name='extras_list')
def extras_list(extras):
    items_list = []
    for item in extras:
        items_list.append(item.extra.id)
    return items_list

@register.filter(name='extra_quantity')
def extra_quantity(extras, item_id):
    for item in extras:
        if item.extra.id == item_id:
            return item.quantity
    return 1
