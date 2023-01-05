# Generated by Django 4.1.5 on 2023-01-03 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="JobHunter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("contact_no", models.CharField(max_length=255)),
                ("qualification", models.CharField(max_length=255)),
                ("experience", models.TextField()),
                ("skills", models.TextField()),
                (
                    "resume",
                    models.FileField(blank=True, null=True, upload_to="resumes/"),
                ),
            ],
        ),
    ]