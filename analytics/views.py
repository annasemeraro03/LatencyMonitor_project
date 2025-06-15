from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count
from .models import LoginRecord
from issues.models import Issue  # importa il modello Issue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class LoginStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        three_days_ago = today - timedelta(days=3)

        total_today = (
            LoginRecord.objects
            .filter(timestamp__date=today)
            .count()
        )

        total_today_no_admin = LoginRecord.objects.filter(
            timestamp__date=today
        ).exclude(
            user__is_superuser=True
        ).count()

        login_data = (
            LoginRecord.objects
            .filter(timestamp__date__gte=three_days_ago)
            .annotate(day=TruncDate('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('-day')
        )

        resolved_today = Issue.objects.filter(
            is_resolved=True,
            resolved_at=today
        ).count()

        context['total_today'] = total_today
        context['total_today_no_admin'] = total_today_no_admin
        context['login_stats'] = login_data
        context['resolved_today'] = resolved_today  # passa al template
        return context
