from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, UserUpdateForm

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        registration_sent = request.GET.get('registration_sent') == '1'
        return render(request, 'users/register.html', {'form': form, 'registration_sent': registration_sent})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_researcher = True
            user.save()
            return redirect('/users/register/?registration_sent=1')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_approved:
                login(request, user)
                return redirect('core:home')
            else:
                return render(request, 'users/login.html', {'error': 'Il tuo account non è stato ancora abilitato.', 'is_admin': False})
        return render(request, 'users/login.html', {'error': 'Credenziali non valide.', 'is_admin': False})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:home')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile.html', {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(request, 'users/profile.html', {'form': form})

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