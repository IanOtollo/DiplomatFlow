from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with crispy forms styling."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control mb-3'),
            Field('password', css_class='form-control mb-3'),
            Submit('submit', 'Sign In', css_class='btn btn-primary btn-lg w-100')
        )


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    department = forms.ChoiceField(choices=User.DEPARTMENT_CHOICES, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'department', 
                 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('department', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-3'),
                Column('password2', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Create Account', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "users:login" %}" class="btn btn-outline-secondary btn-lg ms-2">Cancel</a>'),
            )
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.department = self.cleaned_data['department']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form."""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    department = forms.ChoiceField(choices=User.DEPARTMENT_CHOICES, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'department', 
                 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('department', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Update Profile', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "users:profile" %}" class="btn btn-outline-secondary btn-lg ms-2">Cancel</a>'),
            )
        )


class UserProfileForm(forms.ModelForm):
    """User profile form for updating profile information."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 
                 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('department', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('profile_picture', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Update Profile', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "users:profile" %}" class="btn btn-outline-secondary btn-lg ms-2">Cancel</a>'),
            )
        )
