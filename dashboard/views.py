from django.shortcuts import render

# Create your views here.
def view(request):
    # Qui metti la logica per mostrare la lista degli esperimenti
    return render(request, 'dashboard/view.html')

def statistics(request):
    # Qui metti la logica per mostrare le statistiche degli esperimenti
    return render(request, 'dashboard/statistics.html')