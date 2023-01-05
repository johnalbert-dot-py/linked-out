from django.urls import path

from .views import (
    ListOfJobsView,
    CreateJobVacancy,
    UpdateJobVacancy,
    DeactivateJobVacancy,
    ActivateJobVacancy,
    DeleteJobView,
    ListOfApplicantsOnJobView,
    ViewApplicantAsForm,
)

urlpatterns = [
    path("jobs/", ListOfJobsView.as_view(), name="provider-job-listing"),
    path(
        "jobs/create/", CreateJobVacancy.as_view(), name="provider-create-job-vacancy"
    ),
    path(
        "jobs/<int:pk>/update/",
        UpdateJobVacancy.as_view(),
        name="provider-update-job-vacancy",
    ),
    path(
        "jobs/<int:pk>/deactivate/",
        DeactivateJobVacancy.as_view(),
        name="provider-deactivate-job-vacancy",
    ),
    path(
        "jobs/<int:pk>/activate/",
        ActivateJobVacancy.as_view(),
        name="provider-activate-job-vacancy",
    ),
    path(
        "jobs/<int:pk>/delete/",
        DeleteJobView.as_view(),
        name="provider-delete-job-vacancy",
    ),
    path(
        "jobs/<int:pk>/applicants/",
        ListOfApplicantsOnJobView.as_view(),
        name="provider-job-applicants",
    ),
    path(
        "jobs/<int:pk>/applicants/<int:applicant_pk>/",
        ViewApplicantAsForm.as_view(),
        name="provider-job-applicant-view",
    ),
]
