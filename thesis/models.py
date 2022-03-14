from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    class Source(models.TextChoices):
        WEB_SITE = "WEB_SITE"
        CALL_CENTER = "CALL_CENTER"

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now=True)

    # TODO: for website we should take it from cookie?
    google_analytics_id = models.CharField(
        max_length=255, verbose_name="Google Analytics ID", null=True
    )

    utm_campaign = models.CharField(max_length=255, null=True)

    utm_content = models.CharField(max_length=255, null=True)

    utm_medium = models.CharField(max_length=255, null=True)

    utm_source = models.CharField(max_length=255, null=True)

    utm_term = models.CharField(max_length=255, null=True)

    source = models.CharField(max_length=255, choices=Source.choices, null=True)

    ip = models.CharField(max_length=255, null=True)

    phone = PhoneNumberField(null=True, unique=True, verbose_name="Телефон")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    client = models.ForeignKey(Client, related_name="orders", on_delete=models.CASCADE)
