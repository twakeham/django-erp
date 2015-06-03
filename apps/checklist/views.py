from django.shortcuts import render, get_object_or_404
from core.generic.views.single import GenericCreateView

from core.form.models import ModelForm
from models import Checklist

class ChecklistView(GenericCreateView):
    template = 'checklist/checklist.html'
    post_save_redirect = 'http://203.31.49.126/admin'


def show_checklist(request, name):
    model_form = get_object_or_404(ModelForm, name=name)
    #return render(request, 'checklist/checklist.html', {'form': model_form.form})
    return ChecklistView(form=model_form.form, model=model_form.model.model)(request)