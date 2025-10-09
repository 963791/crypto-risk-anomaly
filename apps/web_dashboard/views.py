# apps/web_dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from apps.transactions.models import Transaction
import json

@login_required
def dashboard(request):
    # Basic stats
    total = Transaction.objects.count()
    high_risk = Transaction.objects.filter(risk_label__iexact='HIGH').count()
    medium_risk = Transaction.objects.filter(risk_label__iexact='MEDIUM').count()
    low_risk = Transaction.objects.filter(risk_label__iexact='LOW').count()
    anomalies = Transaction.objects.filter(is_anomaly=True).count()

    # Recent transactions (last 10)
    recent_transactions = Transaction.objects.order_by('-timestamp')[:10]

    # Daily transaction trend for last 7 days
    daily_qs = (
        Transaction.objects
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(count=Count('id'),
                  high_risk_count=Count('id', filter=Q(risk_label__iexact='HIGH')))
        .order_by('-date')[:7]
    )
    # Convert to list of dicts for JS (reverse to chronological)
    daily_stats = list(reversed(list(daily_qs)))

    risk_distribution = {
        'HIGH': high_risk,
        'MEDIUM': medium_risk,
        'LOW': low_risk,
    }

    context = {
        'total_transactions': total,
        'high_risk_count': high_risk,
        'medium_risk_count': medium_risk,
        'low_risk_count': low_risk,
        'anomalies_count': anomalies,
        'recent_transactions': recent_transactions,
        'daily_stats': json.dumps(daily_stats, default=str),
        'risk_distribution': json.dumps(risk_distribution),
    }
    return render(request, 'dashboard/dashboard.html', context)
