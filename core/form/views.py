from django.shortcuts import render
# from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
#
# from models import *
# from signals import form_pre_save, form_post_save
#

#
# def show_form(request, id):
#     form_spec = get_object_or_404(ModelForm, id=id)
#     formclass = _create_form(form_spec)
#
#     if request.method == 'POST':
#         form = formclass(request.POST)
#
#         if form.is_valid():
#             record = form.save(commit=False)
#             form_pre_save.send(form, record=record, request=request)
#             record.save()
#             form_post_save.send(form, record=record, request=request)
#             return HttpResponseRedirect('google.com')
#
#     else:
#         form = formclass()
#
#     return render

from models import *

def show(request):

    formclass = ModelForm.objects.get(name='Contact').form

    if request.method == 'POST':
        form = formclass(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('google.com')

    else:
        form = formclass()

    return render(request, 'form/basic.html', {
        'form': form
    })
