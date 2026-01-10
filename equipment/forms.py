from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions
from .models import ICTEquipment, DeviceAssignment, Directorate, DeviceIssue

User = get_user_model()


class ICTEquipmentForm(forms.ModelForm):
    """Form for creating and editing ICT equipment."""
    
    class Meta:
        model = ICTEquipment
        fields = [
            'equipment_type', 'brand', 'model', 'serial_number', 'asset_tag',
            'purchase_date', 'purchase_price', 'supplier', 'warranty_expiry',
            'condition', 'status', 'specifications', 'notes'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
            'specifications': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('equipment_type', css_class='col-md-6'),
                Column('brand', css_class='col-md-6'),
            ),
            Row(
                Column('model', css_class='col-md-6'),
                Column('serial_number', css_class='col-md-6'),
            ),
            Row(
                Column('asset_tag', css_class='col-md-6'),
                Column('condition', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('purchase_date', css_class='col-md-6'),
            ),
            Row(
                Column('purchase_price', css_class='col-md-6'),
                Column('warranty_expiry', css_class='col-md-6'),
            ),
            'supplier',
            'specifications',
            'notes',
            FormActions(
                Submit('submit', 'Save Equipment', css_class='btn btn-primary'),
                HTML('<a href="{% url "equipment:equipment_list" %}" class="btn btn-secondary">Cancel</a>'),
            )
        )


class DeviceAssignmentForm(forms.ModelForm):
    """Form for assigning devices to directorates."""
    
    class Meta:
        model = DeviceAssignment
        fields = [
            'equipment', 'directorate', 'assigned_to', 'room_number',
            'office_location', 'assignment_notes'
        ]
        widgets = {
            'assignment_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['equipment'].queryset = ICTEquipment.objects.filter(status='available')
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'equipment',
            Row(
                Column('directorate', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6'),
            ),
            Row(
                Column('room_number', css_class='col-md-6'),
                Column('office_location', css_class='col-md-6'),
            ),
            'assignment_notes',
            FormActions(
                Submit('submit', 'Assign Device', css_class='btn btn-primary'),
                HTML('<a href="{% url "equipment:assignment_list" %}" class="btn btn-secondary">Cancel</a>'),
            )
        )


class DirectorateForm(forms.ModelForm):
    """Form for creating and editing directorates."""
    
    class Meta:
        model = Directorate
        fields = ['name', 'code', 'description', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('code', css_class='col-md-6'),
            ),
            'location',
            'description',
            FormActions(
                Submit('submit', 'Save Directorate', css_class='btn btn-primary'),
                HTML('<a href="{% url "equipment:directorate_list" %}" class="btn btn-secondary">Cancel</a>'),
            )
        )


class DeviceIssueForm(forms.ModelForm):
    """Form for reporting device issues."""
    
    class Meta:
        model = DeviceIssue
        fields = ['equipment', 'title', 'description', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filter to only show assigned equipment
        self.fields['equipment'].queryset = ICTEquipment.objects.filter(
            status='assigned'
        ).distinct()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'equipment',
            'title',
            'description',
            'severity',
            FormActions(
                Submit('submit', 'Report Issue', css_class='btn btn-primary'),
                HTML('<a href="{% url "equipment:issue_list" %}" class="btn btn-secondary">Cancel</a>'),
            )
        )


class DeviceIssueResolutionForm(forms.ModelForm):
    """Form for resolving device issues."""
    
    class Meta:
        model = DeviceIssue
        fields = ['status', 'resolution_notes']
        widgets = {
            'resolution_notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'status',
            'resolution_notes',
            FormActions(
                Submit('submit', 'Update Issue', css_class='btn btn-primary'),
            )
        )

