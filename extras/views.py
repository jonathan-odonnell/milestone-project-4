from django.shortcuts import render
from .models import Extra

def extras(request):

    extras = Extra.objects.all()

    context = {
        'extras': extras
    }

    return render(request, 'extras/extras.html', context)
