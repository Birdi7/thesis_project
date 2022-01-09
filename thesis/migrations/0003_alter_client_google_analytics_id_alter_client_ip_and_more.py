# Generated by Django 4.0.1 on 2022-01-09 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0002_client_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='google_analytics_id',
            field=models.CharField(max_length=255, null=True, verbose_name='Google Analytics ID'),
        ),
        migrations.AlterField(
            model_name='client',
            name='ip',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='utm_campaign',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='utm_content',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='utm_medium',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='utm_source',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='utm_term',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
