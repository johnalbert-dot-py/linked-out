from typing import Any
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from user_profile.models import CICTUser


class UserUpdateForm(ModelForm):

    user_profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def is_valid(self):
        result = super().is_valid()
        for x in self.fields if "__all__" in self.errors else self.errors:
            attrs = self.fields[x].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
            attrs.update({"autofocus": True})
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"

    def clean_username(self):
        username = self.cleaned_data["username"]
        if username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email != self.instance.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            if self.cleaned_data["user_profile_picture"]:
                user_profile = CICTUser.objects.get(user=user)
                user_profile.profile_picture = self.cleaned_data["user_profile_picture"]
                user_profile.save()
            user.save()

        return super().save(commit)


class UserPasswordUpdateForm(ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Old Password",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="New Password",
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ["password", "new_password", "confirm_new_password"]

    def is_valid(self):
        result = super().is_valid()
        for x in self.fields if "__all__" in self.errors else self.errors:
            attrs = self.fields[x].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
            attrs.update({"autofocus": True})
        return result

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.instance.check_password(password):
            raise forms.ValidationError("Incorrect password")
        return password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data["new_password"]
        confirm_new_password = self.cleaned_data["confirm_new_password"]
        if new_password != confirm_new_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_new_password

    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()

        return super().save(commit)
