from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import ICTEquipment, DeviceAssignment, Directorate, DeviceHistory, DeviceIssue
from .forms import ICTEquipmentForm, DeviceAssignmentForm, DirectorateForm, DeviceIssueForm, DeviceIssueResolutionForm


class EquipmentListView(LoginRequiredMixin, ListView):
    """List all ICT equipment."""
    model = ICTEquipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ICTEquipment.objects.select_related('created_by').prefetch_related('assignments')
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        condition = self.request.GET.get('condition', '')
        
        if search:
            queryset = queryset.filter(
                Q(brand__icontains=search) |
                Q(model__icontains=search) |
                Q(serial_number__icontains=search) |
                Q(asset_tag__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        if condition:
            queryset = queryset.filter(condition=condition)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_equipment'] = ICTEquipment.objects.count()
        context['available_count'] = ICTEquipment.objects.filter(status='available').count()
        context['assigned_count'] = ICTEquipment.objects.filter(status='assigned').count()
        context['in_repair_count'] = ICTEquipment.objects.filter(status='in_repair').count()
        return context


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    """View equipment details."""
    model = ICTEquipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_assignment'] = self.object.get_current_assignment()
        context['history'] = self.object.history.all()[:10]
        context['issues'] = self.object.issues.filter(status__in=['reported', 'in_progress'])
        return context


class EquipmentCreateView(LoginRequiredMixin, CreateView):
    """Create new equipment."""
    model = ICTEquipment
    form_class = ICTEquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:equipment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'ICT Equipment recorded successfully!')
        return super().form_valid(form)


class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    """Update equipment."""
    model = ICTEquipment
    form_class = ICTEquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:equipment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipment updated successfully!')
        return super().form_valid(form)


class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete equipment with confirmation."""
    model = ICTEquipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment:equipment_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Equipment deleted successfully!')
        return super().delete(request, *args, **kwargs)


class DirectorateListView(LoginRequiredMixin, ListView):
    """List all directorates."""
    model = Directorate
    template_name = 'equipment/directorate_list.html'
    context_object_name = 'directorates'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for directorate in context['directorates']:
            directorate.device_count = directorate.assignments.filter(is_active=True).count()
        return context


class DirectorateCreateView(LoginRequiredMixin, CreateView):
    """Create new directorate."""
    model = Directorate
    form_class = DirectorateForm
    template_name = 'equipment/directorate_form.html'
    success_url = reverse_lazy('equipment:directorate_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Directorate created successfully!')
        return super().form_valid(form)


class DirectorateUpdateView(LoginRequiredMixin, UpdateView):
    """Update directorate."""
    model = Directorate
    form_class = DirectorateForm
    template_name = 'equipment/directorate_form.html'
    success_url = reverse_lazy('equipment:directorate_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Directorate updated successfully!')
        return super().form_valid(form)


class DirectorateDeleteView(LoginRequiredMixin, DeleteView):
    """Delete directorate with confirmation."""
    model = Directorate
    template_name = 'equipment/directorate_confirm_delete.html'
    success_url = reverse_lazy('equipment:directorate_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Directorate deleted successfully!')
        return super().delete(request, *args, **kwargs)


class AssignmentListView(LoginRequiredMixin, ListView):
    """List all device assignments."""
    model = DeviceAssignment
    template_name = 'equipment/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = DeviceAssignment.objects.select_related(
            'equipment', 'directorate', 'assigned_to', 'issued_by'
        ).filter(is_active=True)
        
        directorate = self.request.GET.get('directorate', '')
        if directorate:
            queryset = queryset.filter(directorate_id=directorate)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['directorates'] = Directorate.objects.all()
        return context


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    """Assign device to directorate."""
    model = DeviceAssignment
    form_class = DeviceAssignmentForm
    template_name = 'equipment/assignment_form.html'
    success_url = reverse_lazy('equipment:assignment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            try:
                initial['equipment'] = ICTEquipment.objects.get(pk=equipment_id)
            except ICTEquipment.DoesNotExist:
                pass
        return initial
    
    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.issued_by = self.request.user
        
        # Create history entry
        DeviceHistory.objects.create(
            equipment=assignment.equipment,
            assignment=assignment,
            action='assigned',
            to_directorate=assignment.directorate,
            to_room=assignment.room_number,
            performed_by=self.request.user,
            notes=assignment.assignment_notes
        )
        
        # Update equipment status
        assignment.equipment.status = 'assigned'
        assignment.equipment.save()
        
        assignment.save()
        messages.success(self.request, 'Device assigned successfully!')
        return redirect(self.success_url)


class AssignmentReturnView(LoginRequiredMixin, UpdateView):
    """Return a device from assignment."""
    model = DeviceAssignment
    fields = []
    template_name = 'equipment/assignment_return.html'
    success_url = reverse_lazy('equipment:assignment_list')
    
    def form_valid(self, form):
        assignment = self.get_object()
        assignment.deactivate()
        
        # Create history entry
        DeviceHistory.objects.create(
            equipment=assignment.equipment,
            assignment=assignment,
            action='returned',
            from_directorate=assignment.directorate,
            from_room=assignment.room_number,
            performed_by=self.request.user,
            notes=f"Device returned from {assignment.directorate}"
        )
        
        # Update equipment status
        assignment.equipment.status = 'available'
        assignment.equipment.save()
        
        messages.success(self.request, 'Device returned successfully!')
        return redirect(self.success_url)


class IssueListView(LoginRequiredMixin, ListView):
    """List all device issues."""
    model = DeviceIssue
    template_name = 'equipment/issue_list.html'
    context_object_name = 'issues'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = DeviceIssue.objects.select_related(
            'equipment', 'reported_by', 'resolved_by', 'assignment'
        )
        
        status = self.request.GET.get('status', '')
        severity = self.request.GET.get('severity', '')
        
        if status:
            queryset = queryset.filter(status=status)
        if severity:
            queryset = queryset.filter(severity=severity)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Detect recurring problems
        context['recurring_issues'] = self._detect_recurring_problems()
        return context
    
    def _detect_recurring_problems(self):
        """Detect recurring problems and suggest solutions."""
        # Find equipment with multiple issues
        equipment_issues = DeviceIssue.objects.values('equipment').annotate(
            issue_count=Count('id')
        ).filter(issue_count__gte=2)
        
        recurring = []
        for item in equipment_issues:
            equipment = ICTEquipment.objects.get(pk=item['equipment'])
            issues = equipment.issues.all()
            
            # Group by issue type/description similarity
            issue_titles = [issue.title.lower() for issue in issues]
            common_words = {}
            for title in issue_titles:
                words = title.split()
                for word in words:
                    if len(word) > 4:  # Ignore short words
                        common_words[word] = common_words.get(word, 0) + 1
            
            if common_words:
                most_common = max(common_words.items(), key=lambda x: x[1])
                if most_common[1] >= 2:
                    recurring.append({
                        'equipment': equipment,
                        'issue_count': item['issue_count'],
                        'pattern': most_common[0],
                        'suggestion': self._generate_suggestion(equipment, most_common[0])
                    })
        
        return recurring
    
    def _generate_suggestion(self, equipment, pattern):
        """Generate automated suggestions based on recurring problems."""
        suggestions = {
            'network': 'Consider network infrastructure upgrade or configuration review',
            'hardware': 'Schedule hardware maintenance or replacement',
            'software': 'Update software or review compatibility issues',
            'power': 'Check power supply and backup systems',
            'performance': 'Consider hardware upgrade or optimization',
            'repair': 'Schedule comprehensive maintenance check',
        }
        
        for key, suggestion in suggestions.items():
            if key in pattern.lower():
                return suggestion
        
        return 'Schedule comprehensive review and maintenance for this equipment'


class IssueCreateView(LoginRequiredMixin, CreateView):
    """Report a device issue."""
    model = DeviceIssue
    form_class = DeviceIssueForm
    template_name = 'equipment/issue_form.html'
    success_url = reverse_lazy('equipment:issue_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            try:
                initial['equipment'] = ICTEquipment.objects.get(pk=equipment_id)
            except ICTEquipment.DoesNotExist:
                pass
        return initial
    
    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.reported_by = self.request.user
        issue.assignment = issue.equipment.get_current_assignment()
        issue.save()
        messages.success(self.request, 'Issue reported successfully!')
        return redirect(self.success_url)


class IssueDetailView(LoginRequiredMixin, DetailView):
    """View issue details."""
    model = DeviceIssue
    template_name = 'equipment/issue_detail.html'
    context_object_name = 'issue'


class IssueResolveView(LoginRequiredMixin, UpdateView):
    """Resolve a device issue."""
    model = DeviceIssue
    form_class = DeviceIssueResolutionForm
    template_name = 'equipment/issue_resolve.html'
    success_url = reverse_lazy('equipment:issue_list')
    context_object_name = 'issue'
    
    def form_valid(self, form):
        if form.cleaned_data['status'] == 'resolved':
            form.instance.resolved_by = self.request.user
            form.instance.resolved_at = timezone.now()
        messages.success(self.request, 'Issue updated successfully!')
        return super().form_valid(form)


class EquipmentDashboardView(LoginRequiredMixin, ListView):
    """Equipment management dashboard."""
    model = ICTEquipment
    template_name = 'equipment/dashboard.html'
    context_object_name = 'equipment_list'
    
    def get_queryset(self):
        return ICTEquipment.objects.select_related('created_by')[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_equipment'] = ICTEquipment.objects.count()
        context['available_count'] = ICTEquipment.objects.filter(status='available').count()
        context['assigned_count'] = ICTEquipment.objects.filter(status='assigned').count()
        context['in_repair_count'] = ICTEquipment.objects.filter(status='in_repair').count()
        context['needs_repair_count'] = ICTEquipment.objects.filter(condition='needs_repair').count()
        
        # Recent assignments
        context['recent_assignments'] = DeviceAssignment.objects.select_related(
            'equipment', 'directorate', 'issued_by'
        ).filter(is_active=True).order_by('-assigned_date')[:5]
        
        # Active issues
        context['active_issues'] = DeviceIssue.objects.filter(
            status__in=['reported', 'in_progress']
        ).select_related('equipment', 'reported_by')[:5]
        
        # Recurring problems
        context['recurring_issues'] = self._detect_recurring_problems()
        
        # Directorate distribution
        context['directorate_stats'] = Directorate.objects.annotate(
            device_count=Count('assignments', filter=Q(assignments__is_active=True))
        ).order_by('-device_count')[:10]
        
        return context
    
    def _detect_recurring_problems(self):
        """Detect recurring problems."""
        equipment_issues = DeviceIssue.objects.values('equipment').annotate(
            issue_count=Count('id')
        ).filter(issue_count__gte=2)
        
        recurring = []
        for item in equipment_issues[:5]:
            equipment = ICTEquipment.objects.get(pk=item['equipment'])
            recurring.append({
                'equipment': equipment,
                'issue_count': item['issue_count'],
                'suggestion': 'Schedule comprehensive maintenance review'
            })
        
        return recurring

