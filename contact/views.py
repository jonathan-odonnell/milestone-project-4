from django.shortcuts import render
from .forms import ContactForm

def contact(request):
    """A view to retun the contact page"""

    form = ContactForm()
    template = 'contact/contact.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)
