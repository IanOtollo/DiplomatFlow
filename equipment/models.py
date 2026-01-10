from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator

User = get_user_model()


class Directorate(models.Model):
    """Directorate model for organizing equipment assignments."""
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, help_text="Short code for the directorate (e.g., PS, AU, ASIA)")
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Physical location/building")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Directorate'
        verbose_name_plural = 'Directorates'
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ICTEquipment(models.Model):
    """ICT Equipment model for tracking devices."""
    
    EQUIPMENT_TYPE_CHOICES = [
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop Computer'),
        ('tablet', 'Tablet'),
        ('printer', 'Printer'),
        ('scanner', 'Scanner'),
        ('monitor', 'Monitor'),
        ('router', 'Router/Switch'),
        ('server', 'Server'),
        ('phone', 'Phone/Handset'),
        ('projector', 'Projector'),
        ('other', 'Other'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('needs_repair', 'Needs Repair'),
        ('decommissioned', 'Decommissioned'),
    ]
    
    # Basic Information
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPE_CHOICES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True, help_text="Unique serial number")
    asset_tag = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Ministry asset tag")
    
    # Purchase Information
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.CharField(max_length=200, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    
    # Current Status
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('in_repair', 'In Repair'),
        ('retired', 'Retired'),
    ], default='available')
    
    # Specifications
    specifications = models.TextField(blank=True, help_text="Technical specifications")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_equipment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ICT Equipment'
        verbose_name_plural = 'ICT Equipment'
    
    def __str__(self):
        return f"{self.get_equipment_type_display()} - {self.brand} {self.model} ({self.serial_number})"
    
    def get_current_assignment(self):
        """Get the current active assignment."""
        return self.assignments.filter(is_active=True).first()
    
    def get_condition_class(self):
        """Return CSS class for condition."""
        condition_classes = {
            'excellent': 'text-success',
            'good': 'text-info',
            'fair': 'text-warning',
            'poor': 'text-danger',
            'needs_repair': 'text-danger fw-bold',
            'decommissioned': 'text-secondary',
        }
        return condition_classes.get(self.condition, 'text-secondary')


class DeviceAssignment(models.Model):
    """Model to track device assignments to directorates and officers."""
    
    equipment = models.ForeignKey(ICTEquipment, on_delete=models.CASCADE, related_name='assignments')
    directorate = models.ForeignKey(Directorate, on_delete=models.SET_NULL, null=True, related_name='assignments')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_devices', help_text="Officer assigned to")
    room_number = models.CharField(max_length=50, blank=True, help_text="Room/Office number")
    office_location = models.CharField(max_length=200, blank=True, help_text="Specific office location")
    
    # Assignment Details
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_equipment', help_text="ICT Officer who issued the device")
    assigned_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Notes
    assignment_notes = models.TextField(blank=True, help_text="Notes about this assignment")
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assigned_date']
        verbose_name = 'Device Assignment'
        verbose_name_plural = 'Device Assignments'
    
    def __str__(self):
        return f"{self.equipment} → {self.directorate} ({self.assigned_date.strftime('%Y-%m-%d')})"
    
    def deactivate(self):
        """Deactivate this assignment."""
        self.is_active = False
        self.return_date = timezone.now()
        self.save()


class DeviceHistory(models.Model):
    """Model to track device movement and changes across rooms and directorates."""
    
    ACTION_CHOICES = [
        ('assigned', 'Assigned'),
        ('relocated', 'Relocated'),
        ('returned', 'Returned'),
        ('repaired', 'Repaired'),
        ('replaced', 'Replaced'),
        ('condition_changed', 'Condition Changed'),
        ('status_changed', 'Status Changed'),
    ]
    
    equipment = models.ForeignKey(ICTEquipment, on_delete=models.CASCADE, related_name='history')
    assignment = models.ForeignKey(DeviceAssignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='history_entries')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    
    # Location Changes
    from_directorate = models.ForeignKey(Directorate, on_delete=models.SET_NULL, null=True, blank=True, related_name='history_from')
    to_directorate = models.ForeignKey(Directorate, on_delete=models.SET_NULL, null=True, blank=True, related_name='history_to')
    from_room = models.CharField(max_length=50, blank=True)
    to_room = models.CharField(max_length=50, blank=True)
    
    # Details
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='equipment_actions')
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Device History'
        verbose_name_plural = 'Device History'
    
    def __str__(self):
        return f"{self.equipment} - {self.get_action_display()} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"


class DeviceIssue(models.Model):
    """Model to track device problems and issues."""
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    equipment = models.ForeignKey(ICTEquipment, on_delete=models.CASCADE, related_name='issues')
    assignment = models.ForeignKey(DeviceAssignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    
    # Issue Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    # Reporting
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    reported_at = models.DateTimeField(default=timezone.now)
    
    # Resolution
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reported_at']
        verbose_name = 'Device Issue'
        verbose_name_plural = 'Device Issues'
    
    def __str__(self):
        return f"{self.equipment} - {self.title} ({self.get_severity_display()})"
    
    def mark_resolved(self, user, notes=""):
        """Mark issue as resolved."""
        self.status = 'resolved'
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save()
    
    def get_severity_class(self):
        """Return CSS class for severity."""
        severity_classes = {
            'low': 'text-info',
            'medium': 'text-warning',
            'high': 'text-danger',
            'critical': 'text-danger fw-bold',
        }
        return severity_classes.get(self.severity, 'text-secondary')

