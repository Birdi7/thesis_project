# Generated by Django 4.0.1 on 2022-03-14 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("thesis", "0006_client_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
