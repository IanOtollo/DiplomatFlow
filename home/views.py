from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from tasks.models import Task
from users.models import CustomUser


def index(request):
    """Home page view."""
    # Get some statistics for the homepage
    total_users = CustomUser.objects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    
    # Get recent tasks for display
    recent_tasks = Task.objects.select_related('created_by', 'assigned_to').order_by('-created_at')[:5]
    
    # Get department statistics
    department_stats = CustomUser.objects.values('department').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    context = {
        'total_users': total_users,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'recent_tasks': recent_tasks,
        'department_stats': department_stats,
    }
    
    return render(request, 'home/index.html', context)


@login_required
def contact(request):
    """Contact page view."""
    context = {
        'page_title': 'Contact Us',
    }
    return render(request, 'home/contact.html', context)


def about(request):
    """About page view."""
    context = {
        'page_title': 'About MOFA Task Tracker',
    }
    return render(request, 'home/about.html', context)


def features(request):
    """Features page view."""
    context = {
        'page_title': 'Features',
    }
    return render(request, 'home/features.html', context)