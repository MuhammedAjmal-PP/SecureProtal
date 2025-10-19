from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    # This method is called when the form is initialized
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Loop through the two fields (username and password)
        for field_name, field in self.fields.items():
            
            # 2. Get the field's label (e.g., 'Username', 'Password')
            label = field.label if field.label else field_name.capitalize()
            
            # 3. Set the placeholder attribute in the widget
            field.widget.attrs.update({
                'placeholder': f'Enter Your {label}',
                'class': 'form-control', # Ensures the Bootstrap class is applied
            })


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Required. Letters only.",
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Required. Letters only.",
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text="Required. Enter a valid email address.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
    
    def __init__(self, *args, **kwargs):
        """
        Dynamically applies the 'form-control' class and sets placeholders 
        for all fields.
        """
        super().__init__(*args, **kwargs)
        
        # Loop through all fields and apply the placeholder/class
        for field_name, field in self.fields.items():
            
            # 1. Generate a clean label for the placeholder text
            # E.g., 'first_name' -> 'First Name'
            label = field.label if field.label else field_name.replace('_', ' ').title()
            
            # 2. Set the placeholder and the Bootstrap class
            field.widget.attrs.update({
                'placeholder': f'Enter Your {label}',
                'class': 'form-control',
            })

    def clean_frist_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name


