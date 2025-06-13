from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from experiments.models import Experiment, Device, LatencyData
import json

class DashboardView(TemplateView):
    template_name = 'dashboard/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Brand distribution
        brand_labels, brand_counts = [], []
        brands = Device.objects.values_list('brand', flat=True).distinct()
        for brand in brands:
            count = Experiment.objects.filter(device__brand=brand).count()
            brand_labels.append(brand)
            brand_counts.append(count)

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
