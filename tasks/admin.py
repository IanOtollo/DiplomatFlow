from django.contrib import admin
from .models import Task, TaskComment, TaskAttachment, ReportRequest


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Task admin."""
    
    list_display = ('title', 'status', 'priority', 'category', 'assigned_to', 'created_by', 'due_date', 'is_urgent', 'created_at')
    list_filter = ('status', 'priority', 'category', 'is_urgent', 'requires_approval', 'is_public', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'room_number')
    list_editable = ('status', 'priority', 'assigned_to')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'priority', 'status')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to', 'reported_by')
        }),
        ('Timing', {
            'fields': ('due_date', 'date_completed', 'estimated_hours', 'actual_hours')
        }),
        ('Additional Info', {
            'fields': ('room_number', 'is_urgent', 'requires_approval', 'is_public')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by', 'assigned_to', 'reported_by')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    """Task comment admin."""
    
    list_display = ('task', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'task__title', 'author__username')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task', 'author')


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    """Task attachment admin."""
    
    list_display = ('filename', 'task', 'uploaded_by', 'file_size', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'task__title', 'uploaded_by__username')
    ordering = ('-uploaded_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task', 'uploaded_by')


@admin.register(ReportRequest)
class ReportRequestAdmin(admin.ModelAdmin):
    """Report request admin."""
    
    list_display = ('title', 'status', 'requested_by', 'assigned_to', 'due_date', 'created_at')
    list_filter = ('status', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'requested_by__username', 'assigned_to__username')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('requested_by', 'assigned_to')