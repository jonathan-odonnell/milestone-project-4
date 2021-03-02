from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Extra
from .forms import ExtraForm
from django.views.decorators.http import require_POST


def extras(request):
    extras = Extra.objects.all()
    form = ExtraForm(prefix="add")
    context = {
        'extras': extras,
        'form': form,
    }

    return render(request, 'extras/extras.html', context)


@require_POST
def add_extra(request):
    form = ExtraForm(request.POST, request.FILES, prefix='add')
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully added extra!')
    else:
        messages.error(
            request, 'Failed to add extra. Please ensure the form is valid.')
    return redirect(reverse('extras'))


def edit_extra(request, extra_id):
    extra = get_object_or_404(Extra, id=extra_id)
    if request.method == 'POST':
        form = ExtraForm(request.POST, request.FILES, instance=extra, prefix='edit')
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated extra!')
        else:
            messages.error(
                request, 'Failed to update extra. Please ensure the form is valid.')
        return redirect(reverse('extras'))
    else:
        form = ExtraForm(prefix="edit", instance=extra)

        template = 'extras/includes/modal.html'
        context = {
            'form': form,
            'extra': extra,
        }

    return render(request, template, context)


def delete_extra(request, extra_id):
    extra = get_object_or_404(Extra, id=extra_id)
    extra.delete()
    messages.success(request, 'Extra deleted!')
    return redirect(reverse('extras'))
