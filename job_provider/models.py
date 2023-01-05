from django.db import models
from user_profile.models import CICTUser


class Job(models.Model):

    status_choices = (
        ("activated", "Activated"),
        ("deactivated", "Deactivated"),
    )

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    salary = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    applicants = models.ManyToManyField("job_hunter.JobHunter", blank=True)
    status = models.CharField(
        max_length=255,
        choices=status_choices,
        null=True,
        blank=False,
        default="activated",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class JobProvider(models.Model):
    user = models.ForeignKey(
        CICTUser, on_delete=models.CASCADE, null=False, blank=False
    )
    company_name = models.CharField(max_length=255, null=False, blank=False)
    company_address = models.CharField(max_length=255, null=False, blank=False)
    company_logo = models.ImageField(upload_to="company_logos", null=True, blank=True)
    # create linekd to parent
    jobs = models.ManyToManyField(Job, blank=True, related_name="job_providers")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
