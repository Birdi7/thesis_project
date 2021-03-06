# Generated by Django 4.0.1 on 2022-01-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
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
                ("name", models.CharField(max_length=255)),
                (
                    "google_analytics_id",
                    models.CharField(max_length=255, verbose_name="Google Analytics ID"),
                ),
                ("utm_campaign", models.CharField(max_length=255)),
                ("utm_content", models.CharField(max_length=255)),
                ("utm_medium", models.CharField(max_length=255)),
                ("utm_source", models.CharField(max_length=255)),
                ("utm_term", models.CharField(max_length=255)),
            ],
        ),
    ]
