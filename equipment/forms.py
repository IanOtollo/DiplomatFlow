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
    """Form for assigning devices to directorates. Fields: Equipment, Directorate, Room number, Assigned to, Office location."""
    
    class Meta:
        model = DeviceAssignment
        fields = [
            'equipment', 'directorate', 'room_number',
            'assigned_to', 'office_location'
        ]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['equipment'].queryset = ICTEquipment.objects.filter(status='available').order_by('equipment_type', 'brand', 'serial_number')
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('last_name', 'first_name')
        self.fields['directorate'].queryset = Directorate.objects.all().order_by('name')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('equipment', css_class='form-select mb-3'),
            Field('directorate', css_class='form-select mb-3'),
            Row(
                Column('room_number', css_class='col-md-6 mb-3'),
                Column('office_location', css_class='col-md-6 mb-3'),
            ),
            Field('assigned_to', css_class='form-select mb-3'),
            FormActions(
                Submit('submit', 'Assign', css_class='btn btn-primary'),
                HTML('<a href="{% url "equipment:assignment_list" %}" class="btn btn-secondary">Cancel</a>'),
            )
        )
    
    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.assignment_notes = ''
        if commit:
            inst.save()
        return inst


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

