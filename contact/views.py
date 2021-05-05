from django.shortcuts import render, HttpResponse
from .forms import ContactForm

def contact(request):
    """A view to retun the contact page"""

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid:
            form.save()
            return HttpResponse(200)

    form = ContactForm()
    template = 'contact/contact.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)
