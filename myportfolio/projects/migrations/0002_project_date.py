# Generated by Django 4.2.5 on 2023-11-23 08:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
