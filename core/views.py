from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorData
from django.utils.timezone import now, timedelta
import json

def home(request):
    # Ottieni gli ultimi 5 dati per l'inizializzazione
    initial_data = SensorData.objects.all().order_by('-timestamp')[:5]
    serialized_data = [{
        "payload": item.payload,
        "timestamp": item.timestamp.isoformat()
    } for item in initial_data]
    
    return render(request, 'core/home.html', {
        'initial_data': serialized_data,
        'has_initial_data': bool(initial_data)  # Aggiunto per il template
    })

def get_realtime_data(request):
    try:
        # Ultimi 2 secondi di dati (aumentato da 1 a 2 per maggiore stabilità)
        data = SensorData.objects.filter(
            timestamp__gte=now()-timedelta(seconds=2)
        ).order_by('timestamp')
        
        payloads = [{
            "topic": item.topic,
            "payload": item.payload,
            "timestamp": item.timestamp.isoformat() 
        } for item in data]
        
        return JsonResponse(payloads, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def about(request):
    return render(request, 'core/about.html')