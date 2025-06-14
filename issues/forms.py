from django import forms
from experiments.models import Device, Experiment
from .models import Issue

class IssueForm(forms.ModelForm):
    brand = forms.ChoiceField(choices=[], required=True)
    model = forms.ChoiceField(choices=[], required=True)
    experiment = forms.ChoiceField(choices=[], required=True)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'brand', 'model', 'experiment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = Device.objects.values_list('brand', flat=True).distinct()
        self.fields['brand'].choices = [('', '---------')] + [(b, b) for b in brands]
        self.fields['model'].choices = [('', '---------')]
        self.fields['experiment'].choices = [('', '---------')]

        # Ricarica modelli se brand è in POST o GET data (per validazione form)
        if 'brand' in self.data:
            brand = self.data.get('brand')
            models = Device.objects.filter(brand=brand).values_list('model', flat=True).distinct()
            self.fields['model'].choices = [('', '---------')] + [(m, m) for m in models]

        # Ricarica esperimenti se brand e model sono in data
        if 'brand' in self.data and 'model' in self.data:
            brand = self.data.get('brand')
            model = self.data.get('model')
            try:
                device = Device.objects.get(brand=brand, model=model)
                experiments = Experiment.objects.filter(device=device)
                self.fields['experiment'].choices = [('', '---------')] + [(str(e.id), str(e)) for e in experiments]
            except Device.DoesNotExist:
                self.fields['experiment'].choices = [('', '---------')]

    def clean_experiment(self):
        experiment_id = self.cleaned_data.get('experiment')
        if not experiment_id:
            raise forms.ValidationError("Seleziona un esperimento valido.")
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Experiment.DoesNotExist:
            raise forms.ValidationError("Esperimento non valido.")
        return experiment
