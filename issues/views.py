from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Issue
from .forms import IssueForm
from experiments.models import Device, Experiment
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from users.models import CustomUser
from django.utils import timezone

class PendingIssuesView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'issues/list.html'
    context_object_name = 'issues'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Issue.objects.filter(status='pending')
        else:
            return Issue.objects.filter(reported_by=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context['pending_issues'] = Issue.objects.filter(status='pending')
        
        user_obj = CustomUser.objects.get(username=user)
        context['issues'] = Issue.objects.filter(reported_by=user_obj.id)
        
        context['approved_open_issues'] = Issue.objects.filter(status='approved', is_resolved=False).order_by('-created_at')
        context['is_admin'] = user.is_superuser
        return context

class ApproveIssueView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, id=issue_id)
        issue.status = 'approved'
        issue.save()
        return JsonResponse({'success': True})


class RejectIssueView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, id=issue_id)
        issue.status = 'rejected'
        issue.save()
        return JsonResponse({'success': True})


@login_required
def get_models(request):
    brand = request.GET.get('brand')
    models = Device.objects.filter(brand=brand).values_list('model', flat=True).distinct()
    return JsonResponse({'models': list(models)})

@login_required
def get_experiments(request):
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    try:
        device = Device.objects.get(brand=brand, model=model)
        experiments = Experiment.objects.filter(device=device)
        data = [{'id': e.id, 'text': str(e)} for e in experiments]
    except Device.DoesNotExist:
        data = []
    return JsonResponse({'experiments': data})

class CreateIssueView(LoginRequiredMixin, View):
    def get(self, request):
        form = IssueForm()
        return render(request, 'issues/create_issue.html', {'form': form})

    def post(self, request):
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.experiment = form.cleaned_data['experiment']
            issue.reported_by = request.user
            issue.status = 'pending'
            issue.save()
            return redirect('issues:list')
        return render(request, 'issues/create_issue.html', {'form': form})
    
class ResolveIssueView(LoginRequiredMixin, View):
    def post(self, request, issue_id):
        issue = get_object_or_404(Issue, id=issue_id)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON non valido")

        if 'resolved' not in data or not isinstance(data['resolved'], bool):
            return HttpResponseBadRequest("Campo 'resolved' mancante o non valido")

        issue.is_resolved = data['resolved']
        issue.resolved_at = timezone.now()
        issue.save()

        return JsonResponse({'success': True, 'resolved': issue.is_resolved})