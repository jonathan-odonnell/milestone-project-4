from django.shortcuts import render, HttpResponse
from .forms import ContactForm


def contact(request):
    """
    A view to display the contact page and
    add customer contacts to the database
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid:
            form.save()
            return HttpResponse(status=200)

    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={
                'full_name': request.user.get_full_name(),
                'email': request.user.email})
        else:
            form = ContactForm()
    template = 'contact/contact.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
