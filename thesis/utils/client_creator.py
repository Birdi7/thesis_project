from dataclasses import dataclass, asdict
from typing import Optional

from thesis.models import Client
from urllib.parse import urlparse, parse_qs


@dataclass
class UtmLabelsInfo:
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_source: Optional[str] = None
    utm_term: Optional[str] = None


# TODO: move to another file
def parse_utm_labels_from_url(url: str) -> UtmLabelsInfo:
    parsed = urlparse(url)
    if not parsed.query:
        # print("! no utm labels")
        return UtmLabelsInfo()
    parsed_query = parse_qs(parsed.query)
    # leave only the first value for each query component
    processed = {k: v[0] for k, v in parsed_query.items()}
    return UtmLabelsInfo(**processed)


class ClientCreator:
    def __init__(self):
        pass

    def process(self, **params):
        return Client.objects.create(**params)

    @classmethod
    def from_request(cls, request):
        referer = request.META["HTTP_REFERER"]
        creation_kwargs = {
            "ip": request.META["REMOTE_ADDR"],
            **asdict(parse_utm_labels_from_url(referer)),
            "source": Client.Source.WEB_SITE
        }

        return cls().process(**creation_kwargs)
