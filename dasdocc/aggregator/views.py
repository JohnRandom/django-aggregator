from django.http import HttpResponseRedirect
from django.db import models
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from dasdocc.aggregator.models import StaticContent, Feed
from dasdocc.aggregator.lib.utils import isiterable

class PlaygroundView(TemplateView):
    template_name = "playground.html"

@login_required
def update_content(request, model=None, next="/", allow_overwrite=True):

    if hasattr(request.GET, 'next') and allow_overwrite:
        next = request.GET['next']
    elif hasattr(request.POST, 'next') and allow_overwrite:
        next = request.POST['next']

    if model is None:
        return HttpResponseRedirect(next)

    if isinstance(model, models.Model):
        for source in model.objects.all():
            source.updater.run()
    elif isiterable(model) and all([issubclass(_model, models.Model)
        for _model in model]):
        for _model in model:
            for source in _model.objects.all():
                source.updater.run()
    else:
        raise TypeError(
            'Content can only be updated on models, found %s instead.' %
            type(model))

    return HttpResponseRedirect(next)