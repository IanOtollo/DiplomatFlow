from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models.functions import TruncMonth, TruncWeek
from .models import Task, TaskComment, TaskAttachment, ReportRequest
from .forms import TaskForm, TaskUpdateForm, TaskCommentForm, TaskAttachmentForm, TaskFilterForm, ReportRequestForm
from users.models import CustomUser


class TaskListView(LoginRequiredMixin, ListView):
    """Task list view with filtering and search."""
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Task.objects.select_related('created_by', 'assigned_to', 'reported_by').order_by('-created_at')
        
        # Apply filters
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            status = form.cleaned_data.get('status')
            priority = form.cleaned_data.get('priority')
            category = form.cleaned_data.get('category')
            assigned_to = form.cleaned_data.get('assigned_to')
            created_by = form.cleaned_data.get('created_by')
            is_urgent = form.cleaned_data.get('is_urgent')
            is_overdue = form.cleaned_data.get('is_overdue')
            
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(room_number__icontains=search)
                )
            
            if status:
                queryset = queryset.filter(status=status)
            
            if priority:
                queryset = queryset.filter(priority=priority)
            
            if category:
                queryset = queryset.filter(category=category)
            
            if assigned_to:
                queryset = queryset.filter(assigned_to=assigned_to)
            
            if created_by:
                queryset = queryset.filter(created_by=created_by)
            
            if is_urgent:
                queryset = queryset.filter(is_urgent=True)
            
            if is_overdue:
                queryset = queryset.filter(
                    due_date__lt=timezone.now(),
                    status__in=['pending', 'in_progress']
                )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        context['view_mode'] = self.request.GET.get('view', 'card')
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Task detail view."""
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        
        # Get comments and attachments
        context['comments'] = task.comments.select_related('author').order_by('created_at')
        context['attachments'] = task.attachments.select_related('uploaded_by').order_by('-uploaded_at')
        
        # Forms
        context['comment_form'] = TaskCommentForm()
        context['attachment_form'] = TaskAttachmentForm()
        context['update_form'] = TaskUpdateForm(instance=task)
        
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Task creation view."""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Task update view."""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    
    def get_success_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Task deletion view."""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def dashboard(request):
    """Dashboard view with statistics and charts."""
    user = request.user
    
    # Get user's tasks
    user_tasks = Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user) | Q(reported_by=user)
    ).distinct()
    
    # Task statistics
    total_tasks = user_tasks.count()
    pending_tasks = user_tasks.filter(status='pending').count()
    in_progress_tasks = user_tasks.filter(status='in_progress').count()
    completed_tasks = user_tasks.filter(status='completed').count()
    overdue_tasks = user_tasks.filter(
        due_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).count()
    urgent_tasks = user_tasks.filter(is_urgent=True, status__in=['pending', 'in_progress']).count()
    
    # Recent tasks
    recent_tasks = user_tasks.order_by('-created_at')[:10]
    
    # Tasks by status
    tasks_by_status = user_tasks.values('status').annotate(count=Count('status')).order_by('status')
    
    # Tasks by priority
    tasks_by_priority = user_tasks.values('priority').annotate(count=Count('priority')).order_by('priority')
    
    # Tasks by category
    tasks_by_category = user_tasks.values('category').annotate(count=Count('category')).order_by('category')
    
    # Monthly task completion trend
    monthly_completed = user_tasks.filter(
        status='completed',
        date_completed__isnull=False
    ).extra(
        select={'month': "strftime('%%Y-%%m', date_completed)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Progress calculations
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    completed_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    in_progress_percentage = (in_progress_tasks / total_tasks * 100) if total_tasks > 0 else 0
    pending_percentage = (pending_tasks / total_tasks * 100) if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Time tracking statistics (using minutes)
    total_estimated_minutes = user_tasks.filter(estimated_minutes__isnull=False).aggregate(
        total=Avg('estimated_minutes')
    )['total'] or 0
    
    total_actual_minutes = user_tasks.filter(actual_minutes__isnull=False).aggregate(
        total=Avg('actual_minutes')
    )['total'] or 0
    
    # Convert minutes to hours for display
    avg_estimated_hours = round(total_estimated_minutes / 60, 1) if total_estimated_minutes else 0
    avg_actual_hours = round(total_actual_minutes / 60, 1) if total_actual_minutes else 0
    
    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'urgent_tasks': urgent_tasks,
        'recent_tasks': recent_tasks,
        'tasks_by_status': list(tasks_by_status),
        'tasks_by_priority': list(tasks_by_priority),
        'tasks_by_category': list(tasks_by_category),
        'monthly_completed': list(monthly_completed),
        'completion_percentage': round(completion_percentage, 1),
        'completed_percentage': round(completed_percentage, 1),
        'in_progress_percentage': round(in_progress_percentage, 1),
        'pending_percentage': round(pending_percentage, 1),
        'overdue_percentage': round(overdue_percentage, 1),
        'avg_estimated_hours': avg_estimated_hours,
        'avg_actual_hours': avg_actual_hours,
        'total_estimated_minutes': int(total_estimated_minutes) if total_estimated_minutes else 0,
        'total_actual_minutes': int(total_actual_minutes) if total_actual_minutes else 0,
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required
def add_comment(request, task_id):
    """Add comment to task."""
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('tasks:task_detail', pk=task_id)


@login_required
def add_attachment(request, task_id):
    """Add attachment to task."""
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        form = TaskAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, 'File uploaded successfully!')
        else:
            messages.error(request, 'Error uploading file.')
    
    return redirect('tasks:task_detail', pk=task_id)


@login_required
def update_task_status(request, task_id):
    """Update task status via AJAX."""
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'status': task.status})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def report_request(request):
    """Report request view."""
    if request.method == 'POST':
        form = ReportRequestForm(request.POST, user=request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.requested_by = request.user
            report.save()
            messages.success(request, 'Report request submitted successfully!')
            return redirect('tasks:task_list')
    else:
        form = ReportRequestForm(user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Request Report',
    }
    return render(request, 'tasks/report_request.html', context)


@login_required
def task_complete(request, task_id):
    """Mark task as complete."""
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        task.status = 'completed'
        task.date_completed = timezone.now()
        task.save()
        messages.success(request, f'Task "{task.title}" has been marked as complete.')
        return redirect('tasks:task_detail', pk=task.pk)
    
    return redirect('tasks:task_detail', pk=task.pk)


@login_required
def task_export(request):
    """Export tasks to CSV."""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Status', 'Priority', 'Category', 'Assigned To', 'Created By', 'Due Date', 'Created At'])
    
    # Get user's tasks
    user_tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user) | Q(reported_by=request.user)
    ).distinct().select_related('assigned_to', 'created_by')
    
    for task in user_tasks:
        writer.writerow([
            task.title,
            task.get_status_display(),
            task.get_priority_display(),
            task.get_category_display(),
            task.assigned_to.get_full_name() if task.assigned_to else '',
            task.created_by.get_full_name(),
            task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else '',
            task.created_at.strftime('%Y-%m-%d %H:%M'),
        ])
    
    return response