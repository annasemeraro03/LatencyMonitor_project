from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Issue

@login_required
def pending_issues_view(request):
    if request.user.is_superuser:
        issues = Issue.objects.filter(status='pending')
    else:
        issues = Issue.objects.filter(reported_by=request.user)
    return render(request, 'issues/list.html', {
        'issues': issues,
        'is_admin': request.user.is_superuser,
    })

@login_required
def approve_issue(request, issue_id):
    if not request.user.is_superuser:
        return redirect('issues:pending_issues')
    issue = get_object_or_404(Issue, id=issue_id)
    issue.status = 'approved'
    issue.save()
    return redirect('issues:pending_issues')

@login_required
def reject_issue(request, issue_id):
    if not request.user.is_superuser:
        return redirect('issues:pending_issues')
    issue = get_object_or_404(Issue, id=issue_id)
    issue.status = 'rejected'
    issue.save()
    return redirect('issues:pending_issues')
