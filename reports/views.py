from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json
import csv

from tasks.models import Task

User = get_user_model()

def admin_required(user):
    """Check if user is admin or staff."""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(admin_required)
def task_analytics(request):
    """Task Analytics Dashboard."""
    # Get task statistics
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    overdue_tasks = Task.objects.filter(
        due_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).count()
    
    # Priority breakdown
    priority_stats = Task.objects.values('priority').annotate(count=Count('priority'))
    
    # Category breakdown
    category_stats = Task.objects.values('category').annotate(count=Count('category'))
    
    # Monthly task creation trend (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_tasks = Task.objects.filter(
        created_at__gte=six_months_ago
    ).extra(
        select={'month': "strftime('%%Y-%%m', created_at)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'priority_stats': list(priority_stats),
        'category_stats': list(category_stats),
        'monthly_tasks': list(monthly_tasks),
    }
    
    return render(request, 'reports/task_analytics.html', context)

@login_required
@user_passes_test(admin_required)
def team_performance(request):
    """Team Performance Dashboard."""
    # Get user performance data
    user_stats = User.objects.annotate(
        total_tasks=Count('assigned_tasks'),
        completed_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='completed')),
        pending_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='pending')),
        in_progress_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='in_progress')),
        overdue_tasks=Count('assigned_tasks', filter=Q(
            assigned_tasks__due_date__lt=timezone.now(),
            assigned_tasks__status__in=['pending', 'in_progress']
        ))
    ).filter(total_tasks__gt=0).order_by('-completed_tasks')
    
    # Calculate completion rates
    for user in user_stats:
        if user.total_tasks > 0:
            user.completion_rate = round((user.completed_tasks / user.total_tasks) * 100, 2)
        else:
            user.completion_rate = 0
    
    # Top performers (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    top_performers = User.objects.annotate(
        recent_completed=Count('assigned_tasks', filter=Q(
            assigned_tasks__status='completed',
            assigned_tasks__date_completed__gte=thirty_days_ago
        ))
    ).filter(recent_completed__gt=0).order_by('-recent_completed')[:5]
    
    context = {
        'user_stats': user_stats,
        'top_performers': top_performers,
    }
    
    return render(request, 'reports/team_performance.html', context)

@login_required
@user_passes_test(admin_required)
def monthly_report(request):
    """Monthly Report Dashboard."""
    # Get current month data
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Monthly statistics
    monthly_tasks = Task.objects.filter(created_at__gte=start_of_month)
    monthly_completed = monthly_tasks.filter(status='completed')
    monthly_pending = monthly_tasks.filter(status='pending')
    monthly_in_progress = monthly_tasks.filter(status='in_progress')
    
    # Task completion rate
    total_monthly = monthly_tasks.count()
    completed_monthly = monthly_completed.count()
    completion_rate = round((completed_monthly / total_monthly * 100), 2) if total_monthly > 0 else 0
    
    # Average completion time
    completed_with_dates = monthly_completed.filter(date_completed__isnull=False)
    if completed_with_dates.exists():
        avg_completion_time = sum([
            (task.date_completed - task.created_at).days 
            for task in completed_with_dates
        ]) / completed_with_dates.count()
    else:
        avg_completion_time = 0
    
    # Priority distribution
    priority_dist = monthly_tasks.values('priority').annotate(count=Count('priority'))
    
    # Category distribution
    category_dist = monthly_tasks.values('category').annotate(count=Count('category'))
    
    # Daily task creation trend
    daily_tasks = []
    for i in range(30):
        date = start_of_month + timedelta(days=i)
        if date <= now:
            count = monthly_tasks.filter(created_at__date=date.date()).count()
            daily_tasks.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
    
    context = {
        'month': now.strftime('%B %Y'),
        'total_monthly': total_monthly,
        'completed_monthly': completed_monthly,
        'pending_monthly': monthly_pending.count(),
        'in_progress_monthly': monthly_in_progress.count(),
        'completion_rate': completion_rate,
        'avg_completion_time': round(avg_completion_time, 1),
        'priority_dist': list(priority_dist),
        'category_dist': list(category_dist),
        'daily_tasks': daily_tasks,
    }
    
    return render(request, 'reports/monthly_report.html', context)

@login_required
@user_passes_test(admin_required)
def export_data(request):
    """Export Data Dashboard."""
    # Get export options
    export_formats = ['CSV', 'JSON', 'Excel']
    
    # Get available data types
    data_types = [
        {'name': 'Tasks', 'description': 'All task data with details'},
        {'name': 'Users', 'description': 'User information and statistics'},
        {'name': 'Task Comments', 'description': 'All task comments and attachments'},
        {'name': 'Performance Metrics', 'description': 'Team performance data'},
    ]
    
    if request.method == 'POST':
        data_type = request.POST.get('data_type')
        format_type = request.POST.get('format')
        
        if data_type == 'Tasks':
            return export_tasks_csv()
        elif data_type == 'Users':
            return export_users_csv()
        elif data_type == 'Task Comments':
            return export_comments_csv()
        elif data_type == 'Performance Metrics':
            return export_performance_csv()
    
    context = {
        'export_formats': export_formats,
        'data_types': data_types,
    }
    
    return render(request, 'reports/export_data.html', context)

def export_tasks_csv():
    """Export tasks data to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Title', 'Description', 'Status', 'Priority', 'Category',
        'Assigned To', 'Created By', 'Due Date', 'Created At', 'Completed At'
    ])
    
    tasks = Task.objects.select_related('assigned_to', 'created_by').all()
    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.description,
            task.get_status_display(),
            task.get_priority_display(),
            task.get_category_display(),
            task.assigned_to.get_full_name() if task.assigned_to else 'Unassigned',
            task.created_by.get_full_name(),
            task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else '',
            task.created_at.strftime('%Y-%m-%d %H:%M'),
            task.date_completed.strftime('%Y-%m-%d %H:%M') if task.date_completed else '',
        ])
    
    return response

def export_users_csv():
    """Export users data to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Username', 'First Name', 'Last Name', 'Email',
        'Is Staff', 'Is Active', 'Date Joined', 'Last Login'
    ])
    
    users = User.objects.all()
    for user in users:
        writer.writerow([
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.email,
            user.is_staff,
            user.is_active,
            user.date_joined.strftime('%Y-%m-%d %H:%M'),
            user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else '',
        ])
    
    return response

def export_comments_csv():
    """Export task comments data to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task_comments_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Task ID', 'Task Title', 'Comment', 'Author', 'Created At'
    ])
    
    # This would need to be implemented if you have a Comment model
    # For now, we'll create a placeholder
    writer.writerow(['No comments model implemented yet'])
    
    return response

def export_performance_csv():
    """Export performance metrics to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="performance_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'User', 'Total Tasks', 'Completed Tasks', 'Pending Tasks',
        'In Progress Tasks', 'Overdue Tasks', 'Completion Rate (%)'
    ])
    
    user_stats = User.objects.annotate(
        total_tasks=Count('assigned_tasks'),
        completed_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='completed')),
        pending_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='pending')),
        in_progress_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='in_progress')),
        overdue_tasks=Count('assigned_tasks', filter=Q(
            assigned_tasks__due_date__lt=timezone.now(),
            assigned_tasks__status__in=['pending', 'in_progress']
        ))
    ).filter(total_tasks__gt=0)
    
    for user in user_stats:
        completion_rate = round((user.completed_tasks / user.total_tasks * 100), 2) if user.total_tasks > 0 else 0
        writer.writerow([
            user.get_full_name() or user.username,
            user.total_tasks,
            user.completed_tasks,
            user.pending_tasks,
            user.in_progress_tasks,
            user.overdue_tasks,
            completion_rate,
        ])
    
    return response