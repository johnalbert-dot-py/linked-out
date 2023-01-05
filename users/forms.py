from typing import Any
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from job_hunter.models import JobHunter
from job_provider.models import JobProvider

from user_profile.models import CICTUser
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    error_css_class = "is-invalid"
    password1: Any = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        ),
    )
    password2: Any = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
    )
    user_type = forms.ChoiceField(
        label="Which one are you?",
        choices=CICTUser.user_types,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "Which one are you?",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "password1",
            "password2",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter First Name",
                    "required": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Last Name",
                    "required": True,
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Email",
                    "required": True,
                }
            ),
        }

    def is_valid(self):
        result = super().is_valid()
        for x in self.fields if "__all__" in self.errors else self.errors:
            attrs = self.fields[x].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
        return result

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return super().clean_password2()

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self) -> str:
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            cict_user = CICTUser.objects.create(
                user=user,
                user_type=self.cleaned_data["user_type"],
            )

            if self.cleaned_data["user_type"] == "job-hunter":
                JobHunter.objects.create(user=cict_user)
            elif self.cleaned_data["user_type"] == "job-provider":
                JobProvider.objects.create(user=cict_user)
            else:
                pass

        return super().save(commit)


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username or Email",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        ),
    )

    def is_valid(self):
        result = super().is_valid()
        for x in self.fields if "__all__" in self.errors else self.errors:
            attrs = self.fields[x].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
            attrs.update({"autofocus": True})
        return result

    def clean_username(self) -> str:
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            if User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username
            else:
                raise forms.ValidationError("Username or Email does not exist")
        return username

    def clean_password(self) -> str:
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("")
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError("Your password is incorrect.")
        return password
