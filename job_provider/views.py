from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages

from job_hunter.models import JobHunter

from .forms import ApplicantViewForm

from job_provider.models import Job, JobProvider
from user_profile.models import CICTUser

# Create your views here.
class ListOfJobsView(LoginRequiredMixin, ListView):
    model = JobProvider
    template_name = "job-provider/list.dj.html"
    context_object_name = "data_lists"
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        cict_user = CICTUser.objects.get(user=self.request.user)
        job_provider = JobProvider.objects.get(user=cict_user)
        data = []
        for job in job_provider.jobs.all().order_by("name"):
            data.append(
                {
                    "inside_data": [
                        job.name,
                        job.description[:40]
                        + ("..." if len(job.description) >= 40 else ""),
                        job.salary,
                        job.location,
                        job.get_status_display(),
                    ],
                    "actions": [
                        f"<a href='{reverse('provider-job-applicants', kwargs={'pk': job.pk})}' class='btn btn-outline-primary mx-0 my-0 btn-sm'>View</a>",
                        f"<a href='{reverse('provider-update-job-vacancy', kwargs={'pk': job.pk})}' class='btn btn-outline-secondary mx-0 my-0 btn-sm'>Edit</a>",
                        f"<a href='{reverse('provider-deactivate-job-vacancy', kwargs={'pk': job.pk})}' class='btn btn-outline-warning mx-0 my-0 btn-sm'>Deactivate</a>"
                        if job.status == "activated"
                        else f"<a href='{reverse('provider-activate-job-vacancy', kwargs={'pk': job.pk})}' class='btn btn-outline-success mx-0 my-0 btn-sm'>Activate</a>",
                        f"<a href='{reverse('provider-delete-job-vacancy', kwargs={'pk': job.pk})}' class='btn btn-outline-danger mx-0 my-0 btn-sm'>Delete</a>",
                    ],
                }
            )
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_of"] = "List of Jobs"
        context["user_type"] = "job-provider"
        context[
            "page_description"
        ] = "You can manage all the jobs here that are posted by your company."
        context["page_title"] = "List of Jobs"
        context["no_data_found"] = "No jobs found."
        context["action_add"] = "Add Job Vacancy"
        context["action_add_url"] = reverse("provider-create-job-vacancy")
        context["table_heads"] = [
            "Title",
            "Description",
            "Salary",
            "Location",
            "Job Status",
            "Actions",
        ]
        return context


class CreateJobVacancy(LoginRequiredMixin, CreateView):
    model = Job
    template_name = "job-provider/job-form.dj.html"
    fields = ["name", "description", "salary", "location"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = "job-provider"
        context[
            "page_description"
        ] = f"You can add job vacancy here for your company by filling the required fields below. Or you can go <a href='{ reverse('provider-job-listing') }'>back</a> to the list of jobs."
        context["add_what"] = "Add New Job Vacancy"
        context["page_title"] = "Create new Job Vacancy"
        context["action_title"] = "Add Job Vacancy"
        context["action_add_url"] = "#"
        return context

    def form_valid(self, form):
        cict_user = CICTUser.objects.get(user=self.request.user)
        job_provider = JobProvider.objects.get(user=cict_user)
        job = form.save(commit=False)
        job.save()
        job_provider.jobs.add(job)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        messages.success(self.request, "Job vacancy has been added successfully.")
        return reverse("provider-job-listing")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter job title"}
        )
        form.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter job description"}
        )
        form.fields["salary"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter salary"}
        )
        form.fields["location"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter location"}
        )
        return form


class UpdateJobVacancy(LoginRequiredMixin, UpdateView):
    model = Job
    template_name = "job-provider/job-form.dj.html"
    fields = ["name", "description", "salary", "location"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = "job-provider"
        context[
            "page_description"
        ] = f"You can update the information of the current job selected by filling the required fields below. Or you can go <a href='{reverse('provider-job-listing')}'>back</a> to the list of jobs."
        context["add_what"] = "Update Job Vacancy"
        context["page_title"] = "Update Job Vacancy"
        context["action_title"] = "Update Job Vacancy"
        context["action_add_url"] = "#"
        return context

    def get_success_url(self) -> str:
        messages.success(self.request, "Job vacancy has been added successfully.")
        return reverse("provider-job-listing")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter job title"}
        )
        form.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter job description"}
        )
        form.fields["salary"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter salary"}
        )
        form.fields["location"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter location"}
        )
        return form


class DeactivateJobVacancy(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            job = Job.objects.get(pk=kwargs["pk"])
            job.status = "deactivated"
            job.save()
            messages.success(request, "Job vacancy has been deactivated successfully.")
        except Exception:
            messages.error(request, "Job vacancy does not exist.")

        return redirect(reverse("provider-job-listing"))


class ActivateJobVacancy(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            job = Job.objects.get(pk=kwargs["pk"])
            job.status = "activated"
            job.save()
            messages.success(request, "Job vacancy has been activated successfully.")
        except Exception:
            messages.error(request, "Job vacancy does not exist.")

        return redirect(reverse("provider-job-listing"))


class DeleteJobView(LoginRequiredMixin, DeleteView):

    template_name = "delete-confirmation.dj.html"
    model = Job

    def get_success_url(self) -> str:
        messages.success(self.request, "Job vacancy has been deleted successfully.")
        return reverse("provider-job-listing")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Job Vacancy"
        context[
            "confirmation_title"
        ] = "You are about to delete this Research, Are you sure?"
        context[
            "confirmation_description"
        ] = f"You are about to delete '{ self.get_object().name }' from list of Jobs of this company. This action is irreversible. Are you sure you want to continue?"  # type: ignore

        return context


class ListOfApplicantsOnJobView(LoginRequiredMixin, ListView):
    template_name = "job-provider/list.dj.html"
    context_object_name = "data_lists"
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        job_provider = Job.objects.get(pk=self.kwargs["pk"])
        data = []
        for applicant in job_provider.applicants.all():
            data.append(
                {
                    "inside_data": [
                        applicant.user.user.first_name
                        + " "
                        + applicant.user.user.last_name,
                        applicant.contact_no,
                        applicant.skills[:30] + "..."
                        if len(applicant.skills) > 30
                        else applicant.skills,
                    ],
                    "actions": [
                        f"<a href='{ reverse('provider-job-applicant-view', kwargs={'pk': job_provider.pk, 'applicant_pk': applicant.pk}) }' class='btn btn-outline-success mx-0 my-0 btn-sm'>View</a>",
                        f"<a href='{ applicant.resume.url if applicant.resume else '#' }' class='btn btn-outline-primary mx-0 my-0 btn-sm'>Download Resume</a>",
                    ],
                }
            )
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_provider = Job.objects.get(pk=self.kwargs["pk"])
        context["list_of"] = f"List of Applicants for Job '{job_provider.name}' "
        context["user_type"] = "job-provider"
        context[
            "page_description"
        ] = "You can manage all the applicants here that are applied one of your job postings."
        context["page_title"] = "List of Applicants for Job"
        context["no_data_found"] = "No Applicants found."
        context["table_heads"] = [
            "Name",
            "Contact Number",
            "Skills",
            "Actions",
        ]
        return context


class ViewApplicantAsForm(LoginRequiredMixin, UpdateView):
    model = JobHunter
    template_name = "job-provider/job-form.dj.html"
    form_class = ApplicantViewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = "job-provider"
        context[
            "page_description"
        ] = f"You can view the information of the current applicant. Or you can go <a href='javascript:window.history.back()'>back</a> to the list of jobs."
        context["add_what"] = "View Applicant"
        context["page_title"] = "View Applicant"
        context["action_add_url"] = "#"
        return context

    def get_success_url(self) -> str:
        messages.success(self.request, "Job applicant has been updated successfully.")
        return reverse("provider-job-listing")

    def get_object(self, queryset=None):
        job = Job.objects.get(pk=self.kwargs["pk"])
        applicant = job.applicants.get(pk=self.kwargs["applicant_pk"])
        return applicant
