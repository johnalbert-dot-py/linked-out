from django.forms import ModelForm
from django import forms
from job_hunter.models import JobHunter


class ApplicantViewForm(ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True})
    )

    def __init__(self, *args, **kwargs):
        super(ApplicantViewForm, self).__init__(*args, **kwargs)
        # set inital values
        self.fields["name"].initial = (
            self.instance.user.user.first_name + " " + self.instance.user.user.last_name
        )
        self.fields["resume"].widget.attrs["readonly"] = True

    class Meta:
        model = JobHunter
        fields = [
            "name",
            "contact_no",
            "qualification",
            "experience",
            "skills",
            "resume",
        ]

        widgets = {
            "contact_no": forms.TextInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "qualification": forms.TextInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "experience": forms.Textarea(
                attrs={"class": "form-control", "readonly": True, "rows": 5}
            ),
            "skills": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                    "rows": 5,
                }
            ),
            "resume": forms.FileInput(
                attrs={"class": "form-control", "readonly": True}
            ),
        }
