# Generated by Django 4.1.5 on 2023-01-03 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_provider", "0004_alter_jobprovider_company_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="status",
            field=models.CharField(
                choices=[("activated", "Activated"), ("deactivated", "Deactivated")],
                max_length=255,
                null=True,
            ),
        ),
    ]
