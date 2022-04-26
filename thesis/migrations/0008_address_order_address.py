# Generated by Django 4.0.1 on 2022-04-09 13:19

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("thesis", "0007_client_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(help_text="location point", null=True, srid=4326),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to="thesis.address"
            ),
        ),
    ]
