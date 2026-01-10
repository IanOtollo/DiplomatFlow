from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, CustomAuthenticationForm
from .models import CustomUser, PasswordResetRequest
from tasks.models import Task


class CustomLoginView(LoginView):
    """Custom login view."""
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name()}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('home:index')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, f'Goodbye, {request.user.get_full_name()}!')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """User registration view."""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)
    

class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view."""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self, queryset=None):
        return self.request.user
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's task statistics
        user_tasks = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user) | Q(reported_by=user)
        ).distinct()
        
        context.update({
            'page_title': 'My Profile',
            'form': UserProfileForm(instance=user),
            'total_tasks': user_tasks.count(),
            'pending_tasks': user_tasks.filter(status='pending').count(),
            'in_progress_tasks': user_tasks.filter(status='in_progress').count(),
            'completed_tasks': user_tasks.filter(status='completed').count(),
            'overdue_tasks': user_tasks.filter(
                due_date__lt=timezone.now(),
                status__in=['pending', 'in_progress']
            ).count(),
            'urgent_tasks': user_tasks.filter(is_urgent=True, status__in=['pending', 'in_progress']).count(),
        })
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """User profile update view."""
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)


@login_required
def dashboard(request):
    """Redirect to tasks dashboard."""
    return redirect('tasks:dashboard')


@login_required
def user_list(request):
    """List all users."""
    users = CustomUser.objects.all().order_by('last_name', 'first_name')
    
    # Get department filter
    department = request.GET.get('department')
    if department:
        users = users.filter(department=department)
    
    # Get search query
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(username__icontains=search)
        )
    
    context = {
        'users': users,
        'departments': CustomUser.DEPARTMENT_CHOICES,
        'selected_department': department,
        'search_query': search,
    }
    return render(request, 'users/user_list.html', context)


@login_required
def user_detail(request, pk):
    """User detail view."""
    user = get_object_or_404(CustomUser, pk=pk)
    
    # Get user's task statistics
    user_tasks = Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user) | Q(reported_by=user)
    ).distinct()
    
    context = {
        'user_profile': user,
        'total_tasks': user_tasks.count(),
        'pending_tasks': user_tasks.filter(status='pending').count(),
        'in_progress_tasks': user_tasks.filter(status='in_progress').count(),
        'completed_tasks': user_tasks.filter(status='completed').count(),
        'overdue_tasks': user_tasks.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count(),
        'urgent_tasks': user_tasks.filter(is_urgent=True, status__in=['pending', 'in_progress']).count(),
    }
    return render(request, 'users/user_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_user_management(request):
    """Admin user management dashboard."""
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Get statistics
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    staff_users = users.filter(is_staff=True).count()
    superusers = users.filter(is_superuser=True).count()
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Department filter
    department = request.GET.get('department', '')
    if department:
        users = users.filter(department=department)
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'superusers': superusers,
        'departments': CustomUser.DEPARTMENT_CHOICES,
        'selected_department': department,
        'search_query': search,
    }
    return render(request, 'users/admin_user_management.html', context)


def password_reset_request(request):
    """Handle password reset requests from users."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(username=username, email=email)
            # Create password reset request
            reset_request = PasswordResetRequest.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            messages.success(request, 'Password reset request submitted successfully. An admin will review your request.')
            return redirect('users:password_reset_done')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user found with that username and email combination.')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
    
    return render(request, 'users/password_reset.html')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def password_reset_requests(request):
    """View password reset requests for admin users."""
    reset_requests = PasswordResetRequest.objects.all().order_by('-requested_at')
    
    # Get statistics
    total_requests = reset_requests.count()
    pending_requests = reset_requests.filter(status='pending').count()
    approved_requests = reset_requests.filter(status='approved').count()
    completed_requests = reset_requests.filter(status='completed').count()
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        reset_requests = reset_requests.filter(status=status_filter)
    
    context = {
        'reset_requests': reset_requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'completed_requests': completed_requests,
        'status_choices': PasswordResetRequest.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'users/password_reset_requests.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_edit_user(request, pk):
    """Admin edit user view."""
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('users:admin_user_management')
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'users/admin_edit_user.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_delete_user(request, pk):
    """Admin delete user view."""
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted successfully.')
        return redirect('users:admin_user_management')
    
    context = {
        'user': user,
    }
    return render(request, 'users/admin_delete_user.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_reset_user_password(request, pk):
    """Admin reset user password view."""
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, f'Password for {user.username} has been reset successfully.')
            return redirect('users:admin_user_management')
        else:
            messages.error(request, 'Passwords do not match or are empty.')
    
    context = {
        'user': user,
    }
    return render(request, 'users/admin_reset_password.html', context)