from django.contrib import admin
from .models import ICTEquipment, DeviceAssignment, Directorate, DeviceHistory, DeviceIssue


@admin.register(Directorate)
class DirectorateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'location', 'created_at']
    search_fields = ['name', 'code', 'location']
    list_filter = ['created_at']


@admin.register(ICTEquipment)
class ICTEquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_type', 'brand', 'model', 'serial_number', 'status', 'condition', 'created_at']
    search_fields = ['brand', 'model', 'serial_number', 'asset_tag']
    list_filter = ['equipment_type', 'status', 'condition', 'created_at']
    readonly_fields = ['created_by', 'created_at', 'updated_at']


@admin.register(DeviceAssignment)
class DeviceAssignmentAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'directorate', 'assigned_to', 'issued_by', 'assigned_date', 'is_active']
    search_fields = ['equipment__brand', 'equipment__model', 'directorate__name', 'assigned_to__username']
    list_filter = ['is_active', 'assigned_date', 'directorate']
    readonly_fields = ['issued_by', 'assigned_date', 'created_at', 'updated_at']


@admin.register(DeviceHistory)
class DeviceHistoryAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'action', 'from_directorate', 'to_directorate', 'performed_by', 'timestamp']
    search_fields = ['equipment__brand', 'equipment__model', 'notes']
    list_filter = ['action', 'timestamp']
    readonly_fields = ['timestamp']


@admin.register(DeviceIssue)
class DeviceIssueAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'title', 'severity', 'status', 'reported_by', 'reported_at']
    search_fields = ['title', 'description', 'equipment__brand', 'equipment__model']
    list_filter = ['severity', 'status', 'reported_at']
    readonly_fields = ['reported_by', 'reported_at', 'created_at', 'updated_at']

