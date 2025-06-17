from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.http import JsonResponse
from .models import Experiment, Device
from .forms import ExperimentForm, ExperimentRemoveForm, DeviceForm, DeviceRemoveForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from django.shortcuts import render
from .forms import EditNotesForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date
from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def get_models(request):
    brand = request.GET.get('brand')
    models = Device.objects.filter(brand=brand).values_list('model', flat=True).distinct()
    return JsonResponse({'models': list(models)})

@login_required
def get_experiments_by_device(request):
    print(request)
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    experiments = Experiment.objects.filter(
        device__brand=brand,
        device__model=model
    )
    data = [
        {"id": exp.id, "label": f"{exp.get_mode_display()} - {exp.created_at.date()} (ID:{exp.id})"}
        for exp in experiments
    ]
    return JsonResponse({'experiments': data})

@login_required
@require_GET
def get_experiment_notes(request):
    experiment_id = request.GET.get("experiment_id")
    try:
        experiment = Experiment.objects.get(id=experiment_id)
        return JsonResponse({"notes": experiment.notes})
    except Experiment.DoesNotExist:
        return JsonResponse({"notes": ""}, status=404)

def experiment_detail(request, pk):
    experiment = get_object_or_404(Experiment, pk=pk)
    photodiode_data = experiment.photodiode_data.order_by('index')
    latency_data = experiment.latency_data.order_by('index')

    photodiode_labels = [d.index for d in photodiode_data]
    photodiode_values = [d.value for d in photodiode_data]
    latency_labels = [d.index for d in latency_data]
    latency_values = [d.value for d in latency_data]

    context = {
        'experiment': experiment,
        'photodiode_data': photodiode_data,
        'latency_data': latency_data,
        'photodiode_labels': photodiode_labels,
        'photodiode_values': photodiode_values,
        'latency_labels': latency_labels,
        'latency_values': latency_values,
    }
    return render(request, 'experiments/experiment_detail.html', context)

def search_experiments(request):
    field = request.GET.get('field')
    value = request.GET.get('value')

    experiments = Experiment.objects.all()

    if field and value:
        if field == 'brand':
            experiments = experiments.filter(device__brand=value)
        elif field == 'model':
            experiments = experiments.filter(device__model=value)
        elif field == 'mode':
            experiments = experiments.filter(mode=value)
        elif field == 'date':
            parsed_date = parse_date(value)
            if parsed_date:
                experiments = experiments.filter(created_at__date=parsed_date)

    brands = Device.objects.values_list('brand', flat=True).distinct()
    models = Device.objects.values_list('model', flat=True).distinct()
    modes = [choice[0] for choice in Experiment.MODE_CHOICES]

    return render(request, 'experiments/search_experiments.html', {
        'experiments': experiments,
        'brands': brands,
        'models': models,
        'modes': modes,
        'selected_field': field,
        'selected_value': value,
    })

class ExperimentListView(LoginRequiredMixin, ListView):
    model = Experiment
    template_name = 'experiments/list.html'
    context_object_name = 'experiments'

    def get_queryset(self):
        return Experiment.objects.all().select_related('device')

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
        brand = form.cleaned_data['brand']
        model = form.cleaned_data['model']
        
        if Device.objects.filter(brand__iexact=brand.strip(), model__iexact=model.strip()).exists():
            return render(self.request, self.template_name, {"form": form, "message": "Dispositivo già presente nel database"})
        
        self.object = form.save()
        return redirect(f"{self.request.path}?created=1")

class ExperimentRemoveView(LoginRequiredMixin, FormView):
    template_name = 'experiments/remove_experiment.html'
    form_class = ExperimentRemoveForm
    success_url = reverse_lazy('experiments:list')

    def form_valid(self, form):
        experiments = form.get_selected_experiments()
        count = experiments.count()

        experiments.delete()
        if count == 1:
            messages.success(self.request, "Esperimento eliminato correttamente.")
        else:
            messages.success(self.request, f"{count} esperimenti eliminati con successo.")
        return redirect(f"{self.request.path}?removed=1")    
    
class EditNotesView(LoginRequiredMixin, FormView):
    template_name = 'experiments/edit_notes.html'
    form_class = EditNotesForm
    success_url = reverse_lazy('experiments:edit_notes')

    def form_valid(self, form):
        experiment = form.cleaned_data['experiment']
        notes = form.cleaned_data['notes']
        experiment.notes = notes
        experiment.save()
        messages.success(self.request, "Note aggiornate correttamente.")
        return redirect(f"{self.request.path}?modified=1")

class SearchExperimentsView(ListView):
    model = Experiment
    template_name = 'experiments/search_experiments.html'
    context_object_name = 'experiments'

    def get_queryset(self):
        qs = super().get_queryset().select_related('device')
        field = self.request.GET.get('field', '')
        value = self.request.GET.get('value', '').strip()

        if field == 'brand' and value:
            qs = qs.filter(device__brand=value)
        elif field == 'model' and value:
            qs = qs.filter(device__model=value)
        elif field == 'mode' and value:
            qs = qs.filter(mode=value)
        elif field == 'date' and value:
            parsed_date = parse_date(value)
            if parsed_date:
                qs = qs.filter(created_at__date=parsed_date)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['brands'] = list(Experiment.objects.values_list('device__brand', flat=True).distinct().order_by('device__brand'))
        context['models'] = list(Experiment.objects.values_list('device__model', flat=True).distinct().order_by('device__model'))
        context['modes'] = list(Experiment.objects.values_list('mode', flat=True).distinct().order_by('mode'))

        context['selected_field'] = self.request.GET.get('field', '')
        context['selected_value'] = self.request.GET.get('value', '')

        return context

class DeviceRemoveView(LoginRequiredMixin, FormView):
    template_name = 'experiments/remove_device.html'
    form_class = DeviceRemoveForm
    success_url = reverse_lazy('experiments:list')

    def form_valid(self, form):
        brand = form.cleaned_data['brand']
        model = form.cleaned_data['model']

        try:
            device = Device.objects.get(brand=brand, model=model)
        except Device.DoesNotExist:
            messages.warning(self.request, "Il dispositivo selezionato non esiste.")
            return redirect(f"{self.request.path}?removed=1")
    
        device.delete()
        return redirect(f"{self.request.path}?removed=1")