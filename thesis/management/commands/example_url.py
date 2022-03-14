from django.conf import settings
from django.core.management import BaseCommand

from pathlib import Path


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        count_file = Path(__file__).parent.resolve() / "count_file.txt"
        count_file.touch(exist_ok=True)
        with count_file.open("r") as fp:
            lines = fp.readlines()
        with count_file.open("a") as fp:
            uuid = f"uuid-{len(lines)}"
            fp.write(uuid + "\n")

        print(
            f"http://{settings.HOST}:8000/?utm_source=best-source-ever&utm_campaign=campaign.123&utm_content=some-content&utm_medium=cpc&ua_client_id={uuid}"
        )
