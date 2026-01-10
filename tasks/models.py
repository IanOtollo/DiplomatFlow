from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Task(models.Model):
    """Task model for MOFA Task Tracker."""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]
    
    CATEGORY_CHOICES = [
        ('administrative', 'Administrative'),
        ('consular', 'Consular'),
        ('protocol', 'Protocol'),
        ('economic', 'Economic'),
        ('political', 'Political'),
        ('legal', 'Legal'),
        ('security', 'Security'),
        ('it', 'Information Technology'),
        ('finance', 'Finance'),
        ('hr', 'Human Resources'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # User relationships
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_tasks')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    room_number = models.CharField(max_length=20, blank=True)
    estimated_minutes = models.PositiveIntegerField(null=True, blank=True, 
                                                   validators=[MinValueValidator(1), MaxValueValidator(9999)])
    actual_minutes = models.PositiveIntegerField(null=True, blank=True,
                                                validators=[MinValueValidator(1), MaxValueValidator(9999)])
    
    # Flags
    is_urgent = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def get_priority_class(self):
        """Return CSS class for priority."""
        priority_classes = {
            'low': 'text-success',
            'medium': 'text-warning',
            'high': 'text-danger',
            'urgent': 'text-danger fw-bold',
        }
        return priority_classes.get(self.priority, 'text-secondary')
    
    def get_status_class(self):
        """Return CSS class for status."""
        status_classes = {
            'pending': 'text-warning',
            'in_progress': 'text-info',
            'completed': 'text-success',
            'cancelled': 'text-secondary',
            'on_hold': 'text-muted',
        }
        return status_classes.get(self.status, 'text-secondary')
    
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and self.status not in ['completed', 'cancelled']:
            return timezone.now() > self.due_date
        return False
    
    def get_progress_percentage(self):
        """Calculate progress percentage based on status."""
        progress_map = {
            'pending': 0,
            'in_progress': 50,
            'completed': 100,
            'cancelled': 0,
            'on_hold': 25,
        }
        return progress_map.get(self.status, 0)


class TaskComment(models.Model):
    """Task comment model."""
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.get_full_name()} on {self.task.title}"


class TaskAttachment(models.Model):
    """Task attachment model."""
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.task.title}"


class ReportRequest(models.Model):
    """Report request model."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_requests')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"