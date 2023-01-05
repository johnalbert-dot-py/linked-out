# Generated by Django 4.1.5 on 2023-01-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_hunter", "0003_remove_jobhunter_applied_jobs"),
        ("job_provider", "0002_jobprovider_applicants"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jobprovider",
            name="applicants",
        ),
        migrations.AddField(
            model_name="job",
            name="applicants",
            field=models.ManyToManyField(blank=True, to="job_hunter.jobhunter"),
        ),
    ]