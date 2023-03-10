# Generated by Django 4.1.5 on 2023-01-03 17:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_hunter", "0004_alter_jobhunter_resume"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobhunter",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2023, 1, 3, 17, 35, 59, 164917, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="jobhunter",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
