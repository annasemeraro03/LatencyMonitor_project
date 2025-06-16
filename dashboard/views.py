import json
from django.views.generic import TemplateView, DetailView
from experiments.models import Experiment, Device, LatencyData
from django.db.models import Count
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
import matplotlib.pyplot as plt
import io
import base64

class DashboardView(TemplateView):
    template_name = 'dashboard/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        brand_data = (
            Device.objects
            .values('brand')
            .annotate(count=Count('id'))
            .order_by('brand')
        )

        brand_labels = [entry['brand'] for entry in brand_data]
        brand_counts = [entry['count'] for entry in brand_data]

        devices = Device.objects.all().order_by('brand', 'model')

        # Dati per confronto foto
        photo_devices = Device.objects.filter(experiments__mode="photo").distinct()
        photo_comparison_data = {}
        for device in photo_devices:
            last_exp = Experiment.objects.filter(device=device, mode="photo").order_by('-created_at').first()
            if last_exp:
                latencies = LatencyData.objects.filter(experiment=last_exp).order_by('index')
                photo_comparison_data[str(device.id)] = {
                    'label': f"{device.brand} {device.model}",
                    'latencies': [ld.value for ld in latencies],
                }

        # Dati per confronto video
        video_devices = Device.objects.filter(experiments__mode="video").distinct()
        video_comparison_data = {}
        for device in video_devices:
            last_exp = Experiment.objects.filter(device=device, mode="video").order_by('-created_at').first()
            if last_exp:
                latencies = LatencyData.objects.filter(experiment=last_exp).order_by('index')
                video_comparison_data[str(device.id)] = {
                    'label': f"{device.brand} {device.model}",
                    'latencies': [ld.value for ld in latencies],
                }

        context.update({
            'devices': devices,
            'devices_photo': photo_devices,
            'devices_video': video_devices,
            'brand_labels': json.dumps(brand_labels),
            'brand_counts': json.dumps(brand_counts),
            'photo_comparison_data': json.dumps(photo_comparison_data),
            'video_comparison_data': json.dumps(video_comparison_data),
        })

        return context

class DeviceDetailView(DetailView):
    model = Device
    template_name = 'dashboard/device_detail.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.object
        experiments = Experiment.objects.filter(device=device).order_by('-created_at')

        chart_data = {}
        for exp in experiments:
            latencies = LatencyData.objects.filter(experiment=exp).order_by('index')
            if latencies.exists():
                chart_data[exp.id] = {
                    'labels': [d.index for d in latencies],
                    'latency': [d.value for d in latencies],
                }

        context.update({
            'experiments': experiments,
            'chart_data_json': json.dumps(chart_data),
            'chart_data': chart_data,
        })
        return context

class DevicePrintView(DetailView):
    model = Device
    template_name = 'dashboard/device_print.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.object
        experiments = Experiment.objects.filter(device=device).order_by('-created_at')

        experiments_data = []
        for exp in experiments:
            latencies = LatencyData.objects.filter(experiment=exp).order_by('index')
            chart_image = None
            if latencies.exists():
                labels = [d.index for d in latencies]
                values = [d.value for d in latencies]

                # Genera grafico con matplotlib
                plt.figure(figsize=(6, 3))
                plt.plot(labels, values, marker='o')
                plt.title(f'Esperimento #{exp.id} - Latenze')
                plt.xlabel('Index')
                plt.ylabel('Latency (ms)')
                plt.tight_layout()

                # Salva in buffer PNG
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)

                # Codifica immagine in base64
                chart_image = base64.b64encode(buf.read()).decode('utf-8')

            experiments_data.append({
                'experiment': exp,
                'chart_image': chart_image,
            })

        context.update({
            'experiments_data': experiments_data,
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        html_string = render_to_string(self.template_name, context)
        with tempfile.NamedTemporaryFile(delete=True) as tmpfile:
            HTML(string=html_string, base_url=self.request.build_absolute_uri()).write_pdf(tmpfile.name)
            tmpfile.seek(0)
            pdf = tmpfile.read()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="device_detail.pdf"'
        return response