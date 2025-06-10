from django.shortcuts import render

def list_experiments(request):
    # Qui metti la logica per mostrare la lista degli esperimenti
    return render(request, 'experiments/list.html')
