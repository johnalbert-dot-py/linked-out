from django.urls import path
from .views import (
    JobProfileSettings,
    JobProviderProfileSettings,
    Profile,
    ChangePassword,
)


urlpatterns = [
    path("", Profile.as_view(), name="profile"),
    path("change-password/", ChangePassword.as_view(), name="change-password"),
    path(
        "job-profile-settings/",
        JobProfileSettings.as_view(),
        name="job-profile-settings",
    ),
    path(
        "job-provider-profile-settings/",
        JobProviderProfileSettings.as_view(),
        name="job-provider-profile-settings",
    ),
]
