from django.contrib import admin

# Register your models here.
from .models import Job, JobProvider

admin.site.register(Job)
admin.site.register(JobProvider)
