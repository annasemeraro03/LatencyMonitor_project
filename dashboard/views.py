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

        # Conteggio dispositivi per brand
        brand_data = (
            Device.objects
            .values('brand')
            .annotate(count=Count('id'))
            .order_by('brand')
        )

        brand_labels = [entry['brand'] for entry in brand_data]
        brand_counts = [entry['count'] for entry in brand_data]

        context.update({
            'devices': Device.objects.all(),
            'brand_labels': json.dumps(brand_labels),
            'brand_counts': json.dumps(brand_counts),
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
