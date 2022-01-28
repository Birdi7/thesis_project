from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print(f"http://{settings.HOST}/?utm_source=best-source-ever")