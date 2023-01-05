from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, View
from django.contrib import messages

from job_provider.models import Job
from user_profile.models import CICTUser
from .models import JobHunter


class ListOfJobs(LoginRequiredMixin, ListView):
    model = Job
    template_name = "job-hunter/main.dj.html"
    context_object_name = "job_providers"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = "job-hunter"
        return context

    def get_queryset(self):
        queryset = []
        if self.request.GET.get("search"):
            name = self.model.objects.filter(
                name__icontains=self.request.GET.get("search")
            )
            description = self.model.objects.filter(
                description__icontains=self.request.GET.get("search")
            )
            for job in self.model.objects.all():
                for company in job.job_providers.all():
                    if self.request.GET.get("search") in company.company_name:
                        queryset.append(job)
            queryset += name | description
            return queryset
        return self.model.objects.filter()


class ApplyToJobView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            job = Job.objects.get(pk=kwargs["pk"])
            user = request.user
            cict_profile = CICTUser.objects.get(user=user)
            job_hunter = JobHunter.objects.get(user=cict_profile)
            if job.applicants.contains(job_hunter):
                messages.warning(
                    request,
                    "You already applied for this job. Please wait for the recuiter to contact you.",
                )
            else:
                job.applicants.add(job_hunter)
                job.save()
                messages.success(
                    request,
                    "Successfully applied to this Job. We'll notice the recuiter for your application.",
                )
        except Exception as e:
            print(e)
            messages.warning(request, "Job vacancy does not exist.")

        return redirect(reverse("job-listing"))
