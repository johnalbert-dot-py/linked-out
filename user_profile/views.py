from django.shortcuts import render
from typing import Optional
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages

from django.contrib.auth.models import User
from job_hunter.models import JobHunter
from job_provider.models import JobProvider
from user_profile.models import CICTUser
from .forms import UserUpdateForm, UserPasswordUpdateForm

# Create your views here.


class Profile(LoginRequiredMixin, UpdateView):
    template_name: str = "profile/profile.dj.html"
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(id=self.request.user.id)  # type: ignore
        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        if self.request.user.is_superuser:  # type: ignore
            context["user_profile"] = None
        else:
            context["user_profile"] = CICTUser.objects.get(user=self.request.user)

        if context["user_profile"] is not None:
            job_hunters = JobHunter.objects.filter(user=context["user_profile"])
            job_providers = JobProvider.objects.filter(user=context["user_profile"])

            if job_hunters.exists():
                context["user_type"] = "job-hunter"
            elif job_providers.exists():
                context["user_type"] = "job-provider"
            else:
                context["user_type"] = ""

        return context

    def get_success_url(self) -> Optional[str]:
        messages.success(self.request, "Profile updated successfully!")
        return self.request.path


class ChangePassword(LoginRequiredMixin, UpdateView):
    template_name: str = "profile/change-password.dj.html"
    model = User
    form_class = UserPasswordUpdateForm

    def get_success_url(self) -> Optional[str]:
        messages.success(self.request, "Password changed successfully!")
        return self.request.path

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(id=self.request.user.id)  # type: ignore
        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        if self.request.user.is_superuser:  # type: ignore
            context["user_profile"] = None
        else:
            context["user_profile"] = CICTUser.objects.get(user=self.request.user)

        if context["user_profile"] is not None:
            job_hunters = JobHunter.objects.filter(user=context["user_profile"])
            job_providers = JobProvider.objects.filter(user=context["user_profile"])

            if job_hunters.exists():
                context["user_type"] = "job-hunter"
            elif job_providers.exists():
                context["user_type"] = "job-provider"
            else:
                context["user_type"] = ""

        return context


class JobProfileSettings(LoginRequiredMixin, UpdateView):
    model = JobHunter
    template_name: str = "profile/profile-settings.dj.html"
    fields = ["contact_no", "qualification", "skills", "experience", "resume"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["contact_no"].widget.attrs["class"] = "form-control"
        form.fields["qualification"].widget.attrs["class"] = "form-control"
        form.fields["skills"].widget.attrs["class"] = "form-control"
        form.fields["skills"].widget.attrs["rows"] = 3
        form.fields["experience"].widget.attrs["class"] = "form-control"
        form.fields["experience"].widget.attrs["rows"] = 3
        form.fields["resume"].widget.attrs["class"] = "form-control"
        return form

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        user = CICTUser.objects.get(user=self.request.user)
        queryset = queryset.filter(user=user)

        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

    def get_success_url(self) -> Optional[str]:
        messages.success(self.request, "Profile settings updated successfully!")
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Job Profile Settings"
        context["action_title"] = "Update Job Profile"
        context["user_type"] = "job-hunter"
        return context


class JobProviderProfileSettings(LoginRequiredMixin, UpdateView):
    model = JobProvider
    template_name: str = "profile/profile-settings.dj.html"
    fields = ["company_name", "company_address", "company_logo"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["company_name"].widget.attrs["class"] = "form-control"
        form.fields["company_address"].widget.attrs["class"] = "form-control"
        form.fields["company_logo"].widget.attrs["class"] = "form-control"
        return form

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        user = CICTUser.objects.get(user=self.request.user)
        queryset = queryset.filter(user=user)

        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

    def get_success_url(self) -> Optional[str]:
        messages.success(self.request, "Company Profile settings updated successfully!")
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = "job-provider"
        context["page_title"] = "Job Provider / Company Settings"
        context["action_title"] = "Update Job / Company Profile"
        return context
