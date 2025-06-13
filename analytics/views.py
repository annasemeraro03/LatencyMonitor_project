from django.shortcuts import render

# Create your views here.
def list(request):
    # Qui metti la logica per mostrare le statistiche degli esperimenti
    return render(request, 'analytics/list.html')