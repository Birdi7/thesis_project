from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        
        print("http://localhost:8000/?utm_source=best-source-ever")