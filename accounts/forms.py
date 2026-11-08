from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import Role, Department

User = get_user_model()

INPUT_CLASS = "form-control"
SELECT_CLASS = "form-select"

class StyledFormMixin:
    def style_fields(self):
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = SELECT_CLASS
            elif isinstance(field.widget, (forms.CheckboxInput,)):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = INPUT_CLASS


class LoginForm(AuthenticationForm, StyledFormMixin):
    username = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={"placeholder": "name@company.com", "autofocus": True}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class UserCreateForm(forms.ModelForm, StyledFormMixin):
    password1 = forms.CharField(label="Temporary password", widget=forms.PasswordInput, help_text="At least 10 characters.")
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "employee_id", "phone", "role", "department", "is_active"]
        widgets = {"is_active": forms.CheckboxInput()}
        help_texts = {"employee_id": "Optional internal staff identifier."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].queryset = Role.objects.order_by("name")
        self.fields["department"].queryset = Department.objects.filter(is_active=True)
        self.style_fields()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") and cleaned.get("password2") and cleaned["password1"] != cleaned["password2"]:
            self.add_error("password2", "The passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "employee_id", "phone", "role", "department", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].queryset = Role.objects.order_by("name")
        self.fields["department"].queryset = Department.objects.filter(is_active=True)
        self.style_fields()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class AdminSetPasswordForm(SetPasswordForm, StyledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class ProfileForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class RoleForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Role
        fields = ["name", "code", "description", "permissions"]
        widgets = {"permissions": forms.Textarea(attrs={"rows": 4, "placeholder": '["users.view", "inventory.view"]'})}
        help_texts = {"permissions": 'Enter a JSON list, e.g. ["users.view", "inventory.view"].'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()

    def clean_permissions(self):
        value = self.cleaned_data.get("permissions")
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise forms.ValidationError("Permissions must be a JSON list of text values.")
        return value


class DepartmentForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Department
        fields = ["name", "code", "description", "is_active"]
        widgets = {"is_active": forms.CheckboxInput()}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
