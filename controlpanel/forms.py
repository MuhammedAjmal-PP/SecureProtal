from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
import re  # Import regex for advanced name validation (optional but good practice)



class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling and custom placeholders
        for field_name, field in self.fields.items():
            label = field.label if field.label else field_name.capitalize()
            field.widget.attrs.update(
                {
                    "placeholder": f"Admin {label}",  # Custom placeholder for admin
                    "class": "form-control",
                }
            )


class AdminUserCreationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150,
        required=True,
        help_text="Required. Letters only.",
    )
    last_name = forms.CharField(
        max_length=150,
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
            "is_active",
            "is_staff",
            "is_superuser",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})
                label = (
                    field.label if field.label else field_name.replace("_", " ").title()
                )
                field.widget.attrs.update(
                    {
                        "placeholder": f"Enter {label}",
                    }
                )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

class AdminUserChangeForm(UserChangeForm):

    first_name = forms.CharField(
        max_length=150,
        required=True,
        help_text="Required. Letters, spaces, and hyphens only.",
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        help_text="Required. Letters, spaces, and hyphens only.",
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
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})

            else:
                field.widget.attrs.update({"class": "form-control"})

                label = (
                    field.label if field.label else field_name.replace("_", " ").title()
                )
                field.widget.attrs.update(
                    {
                        "placeholder": f"Enter {label}",
                    }
                )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        # Regular expression that allows letters, spaces, hyphens, and apostrophes
        if not re.fullmatch(r"^[a-zA-Z\s'-]+$", first_name):
            raise forms.ValidationError(
                "First name should contain only letters, spaces, hyphens, or apostrophes."
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.fullmatch(r"^[a-zA-Z\s'-]+$", last_name):
            raise forms.ValidationError(
                "Last name should contain only letters, spaces, hyphens, or apostrophes."
            )
        return last_name