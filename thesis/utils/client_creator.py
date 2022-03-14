from dataclasses import asdict, dataclass
from typing import Optional
from urllib.parse import parse_qs, urlparse

import phonenumbers

from thesis.models import Client
from thesis.utils.dict import omit


@dataclass
class UtmLabelsInfo:
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_source: Optional[str] = None
    utm_term: Optional[str] = None
    ua_client_id: Optional[str] = None

    def to_dict(self):
        return {
            **omit(asdict(self), ["ua_client_id"]),
            "google_analytics_id": self.ua_client_id,
        }


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
        defaults = {k: v for k, v in params.items() if k != "phone"}
        # print("!!!!!!!! defaults", defaults)
        if "google_analytics_id" in defaults:
            existing = Client.objects.filter(google_analytics_id=defaults["google_analytics_id"]).first()
            if existing:
                for k, v in defaults.items():
                    setattr(existing, k, v)
                existing.save()
                return existing
            else:
                created = Client.objects.create(**defaults)
                return created

        return Client.objects.create(**defaults)

    @classmethod
    def from_order_request(cls, request):
        referer = request.META["HTTP_REFERER"]
        creation_kwargs = {
            "ip": request.META["REMOTE_ADDR"],
            **parse_utm_labels_from_url(referer).to_dict(),
            "source": Client.Source.WEB_SITE,
        }

        return cls().process(**creation_kwargs)

    @classmethod
    def from_callibri_request(cls, request):
        params = {k: v for k, v in request.POST.items()}

        creation_kwargs = {
            k: v
            for k, v in params.items()
            if k
            in [
                "utm_campaign",
                "utm_content",
                "utm_medium",
                "utm_source",
                "utm_term",
            ]
        }
        creation_kwargs["phone"] = phonenumbers.parse(params["phone"], region="RU")
        creation_kwargs["google_analytics_id"] = params.get("ua_client_id")
        return cls().process(**creation_kwargs)
