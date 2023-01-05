from django.db import models
from django.contrib.auth.models import User


class CICTUser(models.Model):

    user_types = (
        ("job-hunter", "Job Hunter"),
        ("job-provider", "Job Provider / Company"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    user_type = models.CharField(
        max_length=50, choices=user_types, null=True, blank=False
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures", null=True, blank=True
    )

    _extra_fields = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        if self.user:
            return self.user.first_name + " " + self.user.last_name  # type: ignore
        else:
            return "No User - " + self.get_user_type_display()  # type: ignore
