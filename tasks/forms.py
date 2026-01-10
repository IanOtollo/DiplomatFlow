from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, FieldWithButtons
from .models import Task, TaskComment, TaskAttachment, ReportRequest
from django.utils import timezone

User = get_user_model()


class TaskForm(forms.ModelForm):
    """Task creation and editing form."""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'assigned_to', 
                 'reported_by', 'due_date', 'room_number', 'estimated_minutes', 
                 'is_urgent', 'requires_approval', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estimated_minutes': forms.NumberInput(attrs={'min': '1', 'max': '9999'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter users by department if user is not admin
        if self.user and not self.user.is_staff:
            self.fields['assigned_to'].queryset = User.objects.filter(
                department=self.user.department
            ).order_by('last_name', 'first_name')
        else:
            self.fields['assigned_to'].queryset = User.objects.all().order_by('last_name', 'first_name')
        
        self.fields['reported_by'].queryset = User.objects.all().order_by('last_name', 'first_name')
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control mb-3'),
            Field('description', css_class='form-control mb-3'),
            Row(
                Column('category', css_class='form-group col-md-4 mb-3'),
                Column('priority', css_class='form-group col-md-4 mb-3'),
                Column('due_date', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('assigned_to', css_class='form-group col-md-6 mb-3'),
                Column('reported_by', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('room_number', css_class='form-group col-md-4 mb-3'),
                Column('estimated_minutes', css_class='form-group col-md-4 mb-3'),
                Column('is_urgent', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('requires_approval', css_class='form-group col-md-6 mb-3'),
                Column('is_public', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Save Task', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "tasks:task_list" %}" class="btn btn-outline-secondary btn-lg ms-2">Cancel</a>'),
            )
        )


class TaskUpdateForm(forms.ModelForm):
    """Task update form for status changes."""
    
    class Meta:
        model = Task
        fields = ['status', 'assigned_to', 'due_date', 'actual_minutes', 'date_completed']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_completed': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'actual_minutes': forms.NumberInput(attrs={'min': '1', 'max': '9999'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('status', css_class='form-group col-md-6 mb-3'),
                Column('assigned_to', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('due_date', css_class='form-group col-md-6 mb-3'),
                Column('actual_minutes', css_class='form-group col-md-6 mb-3'),
            ),
            Field('date_completed', css_class='form-control mb-3'),
            FormActions(
                Submit('submit', 'Update Task', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "tasks:task_detail" task.pk %}" class="btn btn-outline-secondary btn-lg ms-2">Cancel</a>'),
            )
        )


class TaskCommentForm(forms.ModelForm):
    """Task comment form."""
    
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('content', css_class='form-control mb-3'),
            FormActions(
                Submit('submit', 'Add Comment', css_class='btn btn-primary'),
            )
        )


class TaskAttachmentForm(forms.ModelForm):
    """Task attachment form."""
    
    class Meta:
        model = TaskAttachment
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.xls,.xlsx,.txt,.jpg,.jpeg,.png'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('file', css_class='form-control mb-3'),
            FormActions(
                Submit('submit', 'Upload File', css_class='btn btn-primary'),
            )
        )
    
    def save(self, commit=True):
        attachment = super().save(commit=False)
        if self.cleaned_data.get('file'):
            attachment.filename = self.cleaned_data['file'].name
            attachment.file_size = self.cleaned_data['file'].size
        if commit:
            attachment.save()
        return attachment


class ReportRequestForm(forms.ModelForm):
    """Report request form."""
    
    class Meta:
        model = ReportRequest
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter users by department if user is not admin
        if self.user and not self.user.is_staff:
            self.fields['assigned_to'].queryset = User.objects.filter(
                department=self.user.department
            ).order_by('last_name', 'first_name')
        else:
            self.fields['assigned_to'].queryset = User.objects.all().order_by('last_name', 'first_name')
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control mb-3'),
            Field('description', css_class='form-control mb-3'),
            Row(
                Column('assigned_to', css_class='form-group col-md-6 mb-3'),
                Column('due_date', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Request Report', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "tasks:task_list" %}" class="btn btn-outline-secondary btn-lg ms-2">Cancel</a>'),
            )
        )


class TaskFilterForm(forms.Form):
    """Task filtering form."""
    
    STATUS_CHOICES = [('', 'All Statuses')] + Task.STATUS_CHOICES
    PRIORITY_CHOICES = [('', 'All Priorities')] + Task.PRIORITY_CHOICES
    CATEGORY_CHOICES = [('', 'All Categories')] + Task.CATEGORY_CHOICES
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search tasks...', 'class': 'form-control'})
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('last_name', 'first_name'),
        required=False,
        empty_label="All Users",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    created_by = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('last_name', 'first_name'),
        required=False,
        empty_label="All Creators",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_urgent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_overdue = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('search', css_class='form-group col-md-6 mb-3'),
                Column('status', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('priority', css_class='form-group col-md-4 mb-3'),
                Column('category', css_class='form-group col-md-4 mb-3'),
                Column('assigned_to', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('created_by', css_class='form-group col-md-6 mb-3'),
                Column(
                    Div(
                        Field('is_urgent', css_class='form-check-input'),
                        HTML('<label class="form-check-label" for="id_is_urgent">Urgent Only</label>'),
                        css_class='form-check'
                    ),
                    css_class='col-md-3 mb-3'
                ),
                Column(
                    Div(
                        Field('is_overdue', css_class='form-check-input'),
                        HTML('<label class="form-check-label" for="id_is_overdue">Overdue Only</label>'),
                        css_class='form-check'
                    ),
                    css_class='col-md-3 mb-3'
                ),
            ),
            FormActions(
                Submit('submit', 'Filter Tasks', css_class='btn btn-primary'),
                HTML('<a href="{% url "tasks:task_list" %}" class="btn btn-outline-secondary ms-2">Clear Filters</a>'),
            )
        )
