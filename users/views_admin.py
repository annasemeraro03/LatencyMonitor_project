from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
import json

User = get_user_model()

class AdminLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html', {'is_admin': True})
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('core:home')
        return render(request, 'users/login.html', {'error': 'Credenziali non valide.', 'is_admin': True})
    
class AdminUserApprovalView(View):
    def get(self, request):
        pending_users = User.objects.filter(is_approved=False, is_researcher=True)
        return render(request, 'admin/users_approval.html', {'pending_users': pending_users})

    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            action = data.get('action')
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        user = get_object_or_404(User, pk=user_id)

        if action == 'approve':
            user.is_approved = True
            user.save()
            return JsonResponse({'success': f"Utente {user.username} approvato."})
        elif action == 'reject':
            user.delete()
            return JsonResponse({'success': f"Utente {user.username} rifiutato e rimosso."})
        else:
            return JsonResponse({'error': 'Azione non valida'}, status=400)

class AdminUserDetails(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return JsonResponse(data)