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
def next_day(duration):
    if duration.days > 0:
        return f'(+ {duration.days} day)'

@register.filter(name='extra_quantity')
def extra_quantity(extras, item_id):
    for item in extras:
        if item.extra.id == item_id:
            return item.quantity
    return 1
