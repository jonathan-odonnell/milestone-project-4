from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Extra
from .forms import ExtraForm
from django.contrib.auth.decorators import login_required
from holidays.utlis import superuser_required


def extras(request):
    """A view to display all extras."""
    extras = Extra.objects.all()

    template = 'extras/extras.html'
    context = {
        'extras': extras,
    }

    return render(request, template, context)


@login_required
@superuser_required
def add_extra(request):
    """
    A view to display the add extra page and add the extra to the database.
    """
    if request.method == 'POST':
        form = ExtraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added extra!')
            return redirect(reverse('extras'))
        else:
            messages.error(
                request,
                'Failed to add extra. Please ensure the form is valid.')
    else:
        form = ExtraForm()

    template = 'extras/add_extra.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
@superuser_required
def edit_extra(request, extra):
    """
    A view to display the edit extra page and edit the extra in the database.
    """
    extra = get_object_or_404(Extra, slug=extra)
    if request.method == 'POST':
        form = ExtraForm(request.POST, request.FILES, instance=extra)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated extra!')
            return redirect(reverse('extras'))
        else:
            messages.error(
                request,
                'Failed to update extra. Please ensure the form is valid.')
    else:
        form = ExtraForm(instance=extra)

    template = 'extras/edit_extra.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
@superuser_required
def delete_extra(request, extra):
    """A view to delete the extra from the database."""
    extra = get_object_or_404(Extra, slug=extra)
    extra.delete()
    messages.success(request, 'Extra deleted!')
    return redirect(reverse('extras'))
