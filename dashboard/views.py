from django.shortcuts import render

# Create your views here.
def view(request):
    # Qui metti la logica per mostrare la lista degli esperimenti
    return render(request, 'dashboard/view.html')