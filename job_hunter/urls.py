from django.urls import path

from .views import ListOfJobs, ApplyToJobView

urlpatterns = [
    path("", ListOfJobs.as_view(), name="job-listing"),
    path("apply/<int:pk>/", ApplyToJobView.as_view(), name="apply-to-job"),
]
