from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.http import JsonResponse
from .models import Experiment, Device
from .forms import ExperimentForm, ExperimentRemoveForm, DeviceForm, PhotodiodeDataForm, LatencyDataForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from django.shortcuts import render
from .forms import EditNotesForm

@login_required
def get_models(request):
    brand = request.GET.get('brand')
    models = Device.objects.filter(brand=brand).values_list('model', flat=True).distinct()
    return JsonResponse({'models': list(models)})

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
        
        if count == 0:
            messages.warning(self.request, "Nessun esperimento trovato con i criteri selezionati")
        else:
            experiments.delete()
        
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
        return redirect(self.success_url)

@login_required
def get_experiments_by_device(request):
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