from django.db import models


class Client(models.Model):
    class Source(models.TextChoices):
        WEB_SITE = "WEB_SITE"
        CALL_CENTER = "CALL_CENTER"

    name = models.CharField(max_length=255)

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
