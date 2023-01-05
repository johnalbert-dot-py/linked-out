from django.db import models

# Create your models here.
from django.db import models
from user_profile.models import CICTUser

# Create your models here.
class JobHunter(models.Model):
    user = models.ForeignKey(
        CICTUser, on_delete=models.CASCADE, null=False, blank=False
    )
    contact_no = models.CharField(max_length=255, null=False, blank=False)
    qualification = models.CharField(max_length=255, null=False, blank=False)
    experience = models.TextField(null=False, blank=False)
    skills = models.TextField(null=False, blank=False)
    resume = models.FileField(upload_to="resumes", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
