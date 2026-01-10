from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """Custom user model with additional fields."""
    
    DEPARTMENT_CHOICES = [
        ('Admin', 'Administration'),
        ('Diplomacy', 'Diplomacy'),
        ('Consular', 'Consular Services'),
        ('Protocol', 'Protocol'),
        ('Security', 'Security'),
        ('Finance', 'Finance'),
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Legal', 'Legal Affairs'),
        ('Media', 'Media & Communications'),
        ('other', 'Other'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='other')
    phone_number = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class PasswordResetRequest(models.Model):
    """Model to track password reset requests."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_reset_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_reset_requests')
    processed_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-requested_at']
        verbose_name = 'Password Reset Request'
        verbose_name_plural = 'Password Reset Requests'
    
    def __str__(self):
        return f"Password reset request for {self.user.username} - {self.status}"
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
    
    @property
    def is_completed(self):
        return self.status == 'completed'