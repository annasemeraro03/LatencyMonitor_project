from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.http import JsonResponse
from .models import Experiment, Device
from .forms import ExperimentForm, DeviceForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def get_models(request):
    brand = request.GET.get('brand')
    models = Device.objects.filter(brand=brand).values_list('model', flat=True).distinct()
    return JsonResponse({'models': list(models)})

class ExperimentListView(LoginRequiredMixin, ListView):
    model = Experiment
    context_object_name = 'experiments'
    template_name = 'experiments/list.html'

class ExperimentDetailView(LoginRequiredMixin, DetailView):
    model = Experiment
    template_name = 'experiments/detail.html'
    context_object_name = 'experiment'
    pk_url_kwarg = 'experiment_id'

class ExperimentCreateView(LoginRequiredMixin, CreateView):
    model = Experiment
    form_class = ExperimentForm
    template_name = 'experiments/create_experiment.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect(f"{self.request.path}?created=1")

class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'experiments/create_device.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect(f"{self.request.path}?created=1")

