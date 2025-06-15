from django import forms
from .models import Experiment, PhotodiodeData, LatencyData, Device
import csv
from django.db.models import Q
from django.forms.widgets import DateInput

class ExperimentForm(forms.ModelForm):
    brand = forms.ChoiceField(label="Marca", required=True)
    model = forms.ChoiceField(label="Modello", required=True)
    data_file = forms.FileField(required=True, label="Carica file dati (.csv)")

    class Meta:
        model = Experiment
        fields = ['mode', 'notes']
        widgets = {
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = Device.objects.values_list('brand', flat=True).distinct()
        self.fields['brand'].choices = [('', '--- Seleziona brand ---')] + [(b, b) for b in brands]
        self.fields['model'].choices = [('', '--- Seleziona marca ---')]
        
        data = self.data or self.initial
        selected_brand = data.get('brand')
        if selected_brand:
            models_qs = Device.objects.filter(brand=selected_brand).values_list('model', flat=True).distinct()
            self.fields['model'].choices = [('', '--- Seleziona ---')] + [(m, m) for m in models_qs]

    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get('brand')
        model = cleaned_data.get('model')

        if not Device.objects.filter(brand=brand, model=model).exists():
            raise forms.ValidationError("Il dispositivo selezionato non è valido.")

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        brand = cleaned_data['brand']
        model = cleaned_data['model']
        device = Device.objects.get(brand=brand, model=model)

        instance = super().save(commit=False)
        instance.device = device

        uploaded_file = cleaned_data.get('data_file')
        if uploaded_file:
            instance.file_name = uploaded_file.name
            instance.data_file = uploaded_file  # salva il file prima di leggerlo

        if commit:
            instance.save()

        # Riapri il file solo dopo che l'istanza è stata salvata completamente
        if commit and uploaded_file:
            uploaded_file.seek(0)  # resetta il cursore del file
            decoded_file = uploaded_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            first_row = next(reader, None)
            if first_row and first_row[0].lower() == "photodiovalue":
                pass  # header presente
            else:
                reader = [first_row] + list(reader)  # reinserisci la prima riga

            photodiode_objects = []
            latency_objects = []

            for idx, row in enumerate(reader):
                try:
                    pd_value = float(row[0])
                    lat_value = float(row[1])
                except (ValueError, IndexError):
                    continue

                photodiode_objects.append(
                    PhotodiodeData(
                        experiment=instance,
                        index=idx,
                        value=pd_value,
                        timestamp=None
                    )
                )
                latency_objects.append(
                    LatencyData(
                        experiment=instance,
                        index=idx,
                        value=lat_value,
                        timestamp=None
                    )
                )

            # Inserisci i dati in blocco per evitare rallentamenti e lock
            PhotodiodeData.objects.bulk_create(photodiode_objects)
            LatencyData.objects.bulk_create(latency_objects)

        return instance

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['brand', 'model']
        widgets = {
            'brand': forms.TextInput(attrs={'placeholder': 'Es. Samsung'}),
            'model': forms.TextInput(attrs={'placeholder': 'Es. Galaxy S21'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get('brand')
        model = cleaned_data.get('model')
        
        if brand and model:
            cleaned_data['brand'] = brand.strip()
            cleaned_data['model'] = model.strip()
            
        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.brand = instance.brand.strip()
        instance.model = instance.model.strip()
        if commit:
            instance.save()
        return instance


class PhotodiodeDataForm(forms.ModelForm):
    class Meta:
        model = PhotodiodeData
        fields = ['index', 'value', 'timestamp']


class LatencyDataForm(forms.ModelForm):
    class Meta:
        model = LatencyData
        fields = ['index', 'value', 'timestamp']

from django import forms
from .models import Experiment, Device

class ExperimentRemoveForm(forms.Form):
    brand = forms.ChoiceField(
        choices=[],
        required=True,
        label="Marca"
    )
    model = forms.ChoiceField(
        choices=[],
        required=True,
        label="Modello"
    )
    mode = forms.ChoiceField(
        choices=Experiment.MODE_CHOICES,
        required=True,
        label="Modalità"
    )
    experiment = forms.ModelChoiceField(
        queryset=Experiment.objects.none(),
        required=False,
        label="Esperimento (opzionale)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices = self.get_brand_choices()
        self.fields['model'].choices = self.get_model_choices()
        data = self.data or self.initial

        selected_brand = data.get('brand')
        selected_model = data.get('model')
        selected_mode = data.get('mode')

        if selected_brand and selected_model and selected_mode:
            self.fields['experiment'].queryset = Experiment.objects.filter(
                device__brand=selected_brand,
                device__model=selected_model,
                mode=selected_mode
            )
        else:
            self.fields['experiment'].queryset = Experiment.objects.none()

    def get_brand_choices(self):
        brands = Device.objects.values_list('brand', flat=True).distinct()
        return [('', '---')] + [(b, b) for b in brands]

    def get_model_choices(self):
        models = Device.objects.values_list('model', flat=True).distinct()
        return [('', '---')] + [(m, m) for m in models]

    def get_selected_experiments(self):
        # Se è stato scelto un esperimento singolo, restituiscilo in queryset singolo
        experiment = self.cleaned_data.get('experiment')
        if experiment:
            return Experiment.objects.filter(pk=experiment.pk)
        # Altrimenti filtro per brand, model e mode
        brand = self.cleaned_data.get('brand')
        model = self.cleaned_data.get('model')
        mode = self.cleaned_data.get('mode')
        return Experiment.objects.filter(
            device__brand=brand,
            device__model=model,
            mode=mode
        )
        
class EditNotesForm(forms.Form):
    brand = forms.ChoiceField(choices=[], required=True)
    model = forms.ChoiceField(choices=[], required=True)
    experiment = forms.ModelChoiceField(queryset=Experiment.objects.none(), required=True, label="Esperimento")
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Note")

    def __init__(self, *args, **kwargs):
        super(EditNotesForm, self).__init__(*args, **kwargs)

        # Popola i brand unici
        brands = Device.objects.values_list('brand', flat=True).distinct()
        self.fields['brand'].choices = [('', '--- Seleziona ---')] + [(b, b) for b in brands]

        data = self.data or self.initial
        selected_brand = data.get('brand')
        selected_model = data.get('model')

        # Popola i modelli se è stato selezionato un brand
        if selected_brand:
            models = Device.objects.filter(brand=selected_brand).values_list('model', flat=True).distinct()
            self.fields['model'].choices = [('', '--- Seleziona ---')] + [(m, m) for m in models]
        else:
            self.fields['model'].choices = [('', '--- Seleziona un brand prima ---')]

        # Popola esperimenti se brand e modello sono stati selezionati
        if selected_brand and selected_model:
            self.fields['experiment'].queryset = Experiment.objects.filter(
                device__brand=selected_brand,
                device__model=selected_model
            )