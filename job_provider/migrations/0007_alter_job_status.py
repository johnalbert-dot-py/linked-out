# Generated by Django 4.1.5 on 2023-01-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "job_provider",
            "0006_job_created_at_job_updated_at_jobprovider_created_at_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="status",
            field=models.CharField(
                choices=[("activated", "Activated"), ("deactivated", "Deactivated")],
                default="activated",
                max_length=255,
                null=True,
            ),
        ),
    ]
