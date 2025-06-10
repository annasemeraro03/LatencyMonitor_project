from django.shortcuts import render

# Create your views here.
def list_issues(request):
    # Qui metti la logica per mostrare la lista degli esperimenti
    return render(request, 'issues/list.html')